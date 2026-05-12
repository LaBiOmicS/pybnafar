from .downloader import BnafarDownloader
from .processor import BnafarProcessor
from .analytics import BnafarAnalytics
from .diagnostics import BnafarDiagnostics
from .interop import BnafarInterop
from .utils import logger
import os
import glob
import pandas as pd

class Bnafar:
    """
    Main SDK for interacting with the Brazilian National Pharmaceutical Database (BNAFAR).
    Designed for scalability, auditability, and clinical intelligence.
    """
    
    def __init__(self, workspace: str = 'bnafar_system'):
        self.workspace = os.path.abspath(workspace)
        self.raw_dir = os.path.join(self.workspace, 'raw')
        self.lake_dir = os.path.join(self.workspace, 'lake_partitioned')
        self.manifest_dir = os.path.join(self.workspace, 'manifests')
        
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.lake_dir, exist_ok=True)
        os.makedirs(self.manifest_dir, exist_ok=True)
        
        self.downloader = BnafarDownloader(workspace_dir=self.raw_dir)
        self.analytics = BnafarAnalytics()
        self.diagnostics = BnafarDiagnostics()
        self.interop = BnafarInterop()

    def sync(self, use_api: bool = True):
        """
        Synchronizes local Data Lake with official government snapshots.
        Uses Atomic processing to ensure data integrity.
        """
        resources = self.downloader.fetch_sources(use_api=use_api)
        if not resources:
            logger.warning("No data sources found on the portal.")
            return

        for res in resources:
            # Check if this snapshot is already in the lake
            manifest_name = f"manifest_{res['title'].replace(' ', '_')}.json"
            if os.path.exists(os.path.join(self.manifest_dir, manifest_name)):
                logger.debug(f"Snapshot already synchronized: {res['title']}")
                continue
            
            try:
                csv_path = self.downloader.download(res['url'], f"{res['title']}.csv")
                BnafarProcessor.process_and_partition(
                    csv_path=csv_path,
                    output_dir=self.lake_dir,
                    manifest_dir=self.manifest_dir,
                    metadata={'source_url': res['url'], 'snapshot': res['title']}
                )
            except Exception as e:
                logger.error(f"Sync failed for {res['title']}: {e}")

    def load_optimized(self, ufs: list = None, months: list = None) -> pd.DataFrame:
        """
        Loads data using high-performance Hive-partition filtering.
        """
        import pyarrow.dataset as ds
        
        # Check if any parquet files exist recursively
        parquet_files = glob.glob(os.path.join(self.lake_dir, "**/*.parquet"), recursive=True)
        if not os.path.exists(self.lake_dir) or not parquet_files:
            logger.warning("Data Lake is empty. Please run sync() first.")
            return pd.DataFrame()

        dataset = ds.dataset(self.lake_dir, format="parquet", partitioning="hive")
        
        filter_expr = None
        if ufs:
            filter_expr = ds.field("sg_uf").isin(ufs)
        
        if months:
            m_filter = ds.field("ano_mes").isin(months)
            if filter_expr is not None:
                filter_expr = filter_expr & m_filter
            else:
                filter_expr = m_filter
            
        df = dataset.to_table(filter=filter_expr).to_pandas()
        
        # Run automatic diagnostics on load
        self.diagnostics.check_geographic_bias(df)
        return df

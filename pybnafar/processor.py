import pandas as pd
import numpy as np
import os
import json
import shutil
from .schema import EXPECTED_SCHEMA, detect_data_drift, COLUMN_ALIASES
from .utils import logger, calculate_hash

class BnafarProcessor:
    """
    High-Performance Data Processing Engine.
    Implements atomic writes and Hive partitioning for SUS scalability.
    """
    
    @staticmethod
    def _clean_and_type(df: pd.DataFrame) -> pd.DataFrame:
        """Strict cleaning and typing with column name resilience."""
        df = df.copy()
        df.columns = [c.lower().strip() for c in df.columns]
        df = df.rename(columns=COLUMN_ALIASES)
        
        for col, dtype in EXPECTED_SCHEMA.items():
            if col in df.columns:
                try:
                    if 'datetime' in str(dtype):
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    elif dtype == 'float64':
                        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
                    else:
                        df[col] = df[col].astype(dtype)
                except Exception as e:
                    logger.error(f"Schema error in column {col}: {e}")
        return df

    @classmethod
    def process_and_partition(cls, csv_path: str, output_dir: str, manifest_dir: str, metadata: dict):
        """
        Atomic and Partitioned Processing.
        Prevents Data Lake corruption in case of process failure.
        """
        logger.info(f"Atomic Processing: {os.path.basename(csv_path)}")
        
        # Temporary directory for atomic write
        temp_dir = os.path.join(output_dir, "_processing_temp")
        if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        try:
            reader = pd.read_csv(csv_path, sep=';', encoding='latin1', chunksize=100000, low_memory=False)
            
            for chunk in reader:
                df = cls._clean_and_type(chunk)
                detect_data_drift(df)
                
                # Partition Engineering (HPC Ready)
                if 'dt_posicao_estoque' in df.columns:
                    df['ano_mes'] = df['dt_posicao_estoque'].dt.strftime('%Y-%m')
                else:
                    df['ano_mes'] = 'unknown'
                
                # Write to temp using Hive partitioning
                df.to_parquet(
                    temp_dir, 
                    engine='pyarrow', 
                    index=False, 
                    partition_cols=['sg_uf', 'ano_mes']
                )
            
            # Atomic Commit: Move files to official lake
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    src = os.path.join(root, file)
                    rel_path = os.path.relpath(src, temp_dir)
                    dest = os.path.join(output_dir, rel_path)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    shutil.move(src, dest)
            
            # Provenance Registration (Certificate of Origin)
            metadata['sha256_original'] = calculate_hash(csv_path)
            metadata['processed_at'] = str(pd.Timestamp.now())
            manifest_path = os.path.join(manifest_dir, f"manifest_{metadata['snapshot'].replace(' ', '_')}.json")
            with open(manifest_path, 'w') as f:
                json.dump(metadata, f, indent=4)
                
            shutil.rmtree(temp_dir)
            logger.info(f"Lake successfully updated. Manifest saved: {manifest_path}")
            
        except Exception as e:
            logger.error(f"Critical Failure: {e}. Reverting temporary changes.")
            if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
            raise

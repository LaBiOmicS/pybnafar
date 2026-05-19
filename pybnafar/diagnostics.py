import pandas as pd

from .utils import logger


class BnafarDiagnostics:
    """
    Evaluates dataset integrity and ethical representation.
    """

    @staticmethod
    def check_geographic_bias(df: pd.DataFrame):
        """
        Detects under-representation of specific Brazilian regions (Ethical Bias).
        """
        if df.empty:
            return

        coverage = df.groupby("sg_uf")["co_municipio_ibge"].nunique()
        total_muni = df["co_municipio_ibge"].nunique()

        logger.info("--- Data Integrity & Geographic Bias Audit ---")
        logger.warning(
            "ETHICAL NOTICE: Low confidence scores often reflect infrastructure "
            "gaps (lack of internet/staff), not necessarily poor management. "
            "Do not use these scores to justify resource withdrawal."
        )

        for uf, count in coverage.items():
            pct = (count / total_muni) * 100
            if pct < 2.0:
                logger.warning(
                    f"Potential Bias: State {uf} represents only {pct:.2f}% of the municipalities."
                )

        return coverage

    @staticmethod
    def validate_integrity(df: pd.DataFrame):
        """Identifies suspicious data points (Logistical Outliers)."""
        if df.empty:
            return

        # Flagging records with suspiciously high stock volumes
        outliers = df[df["qt_estoque"] > 1_000_000]
        if not outliers.empty:
            logger.warning(
                f"Integrity Alert: {len(outliers)} records found with extreme volumes (>1M units)."
            )
        return outliers

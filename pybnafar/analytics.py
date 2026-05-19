from typing import Dict

import pandas as pd

from .constants import CRITICALITY_WEIGHTS, WEIGHTS


class BnafarAnalytics:
    """
    Analytical and Ethical Intelligence for Public Health.
    """

    @staticmethod
    def calculate_confidence_score(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the Data Confidence Index (DCI) per municipality.

        The score ranges from 0.0 to 1.0, where 1.0 indicates maximum reporting reliability.
        It considers reporting frequency, CNES coverage, and data recency.

        Args:
            df: A pandas DataFrame containing BNAFAR stock data.

        Returns:
            A DataFrame with DCI scores and categorical labels for each municipality.
        """
        if df.empty:
            return pd.DataFrame()

        df = df.copy()
        df["dt_posicao_estoque"] = pd.to_datetime(df["dt_posicao_estoque"])

        # 1. Temporal Consistency (Reporting Frequency)
        total_cycles = df["dt_posicao_estoque"].nunique()
        temporal_freq = (
            df.groupby("co_municipio_ibge")["dt_posicao_estoque"].nunique() / total_cycles
        )

        # 2. Network Coverage (Establishment reporting rate)
        cnes_count = (
            df.groupby(["co_municipio_ibge", "dt_posicao_estoque"])["co_cnes"]
            .nunique()
            .reset_index()
        )
        max_cnes = cnes_count.groupby("co_municipio_ibge")["co_cnes"].max()
        current_cycle = df["dt_posicao_estoque"].max()
        current_cnes = cnes_count[cnes_count["dt_posicao_estoque"] == current_cycle].set_index(
            "co_municipio_ibge"
        )["co_cnes"]
        network_coverage = (current_cnes / max_cnes).fillna(0)

        # 3. Recency (Penalty for delay)
        max_date = df["dt_posicao_estoque"].max()
        last_muni_date = df.groupby("co_municipio_ibge")["dt_posicao_estoque"].max()
        delay_days = (max_date - last_muni_date).dt.days
        recency_score = (1 - (delay_days / 30)).clip(lower=0)

        # Final Weighted Calculation using constants
        score = (
            (temporal_freq * WEIGHTS["temporal_consistency"])
            + (network_coverage * WEIGHTS["network_coverage"])
            + (recency_score * WEIGHTS["recency"])
        )

        muni_info = (
            df[["co_municipio_ibge", "no_municipio", "sg_uf"]]
            .drop_duplicates("co_municipio_ibge")
            .set_index("co_municipio_ibge")
        )

        result = pd.DataFrame(
            {
                "confidence_score": score,
                "historical_frequency": temporal_freq,
                "current_network_coverage": network_coverage,
                "recency_status": recency_score,
            }
        ).join(muni_info)

        result["confidence_category"] = pd.cut(
            result["confidence_score"], bins=[0, 0.3, 0.7, 1.1], labels=["Low", "Medium", "High"]
        )
        return result.sort_values("confidence_score", ascending=False).reset_index()

    @staticmethod
    def detect_real_ruptures(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Distinguishes between stockouts (Confirmed Rupture) and reporting failure (Silence).
        """
        if df.empty:
            return {"confirmed_ruptures": pd.DataFrame(), "reporting_failures": pd.DataFrame()}

        pivot = df.pivot_table(
            index=["sg_uf", "no_municipio", "co_catmat", "ds_produto"],
            columns="dt_posicao_estoque",
            values="qt_estoque",
            aggfunc="sum",
        )

        if pivot.shape[1] < 2:
            return {"confirmed_ruptures": pd.DataFrame(), "reporting_failures": pd.DataFrame()}

        t_minus_1, t = pivot.columns[-2:]
        ruptures = pivot[(pivot[t_minus_1] > 0) & (pivot[t] == 0)]
        silence = pivot[(pivot[t_minus_1] > 0) & (pivot[t].isna())]

        return {
            "confirmed_ruptures": ruptures.reset_index(),
            "reporting_failures": silence.reset_index(),
        }

    @staticmethod
    def calculate_priority_waste(df: pd.DataFrame, days: int = 90) -> pd.DataFrame:
        """
        Ranks stock at risk of expiration weighted by public health criticality.
        """
        if "dias_para_vencer" not in df.columns or df.empty:
            return pd.DataFrame()

        waste_risk = df[(df["dias_para_vencer"] > 0) & (df["dias_para_vencer"] <= days)].copy()

        # Use criticality weights from constants
        waste_risk["critical_weight"] = pd.to_numeric(
            waste_risk["tp_produto"].map(CRITICALITY_WEIGHTS).fillna(1)
        )
        waste_risk["qt_estoque"] = pd.to_numeric(waste_risk["qt_estoque"], errors="coerce").fillna(
            0
        )
        waste_risk["severity_index"] = waste_risk["qt_estoque"] * waste_risk["critical_weight"]

        return (
            waste_risk.groupby(["sg_uf", "no_municipio", "ds_produto"])
            .agg({"qt_estoque": "sum", "severity_index": "sum", "dias_para_vencer": "min"})
            .sort_values("severity_index", ascending=False)
            .reset_index()
        )

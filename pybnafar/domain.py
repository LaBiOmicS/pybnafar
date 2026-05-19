import pandas as pd


class BnafarHealthIntelligence:
    """
    Expertise em Assistência Farmacêutica e Epidemiologia.
    """

    @staticmethod
    def classify_component(df: pd.DataFrame) -> pd.DataFrame:
        """
        Classifica os produtos de acordo com os blocos de financiamento do SUS.
        Baseado na tipagem de produto (B: Básico, E: Especializado, S: Estratégico).
        """
        mapping = {
            "B": "Componente Básico (CBAF)",
            "E": "Componente Especializado (CEAF)",
            "S": "Componente Estratégico (CESAF)",
            "O": "Recurso Próprio/Outros",
        }
        if "tp_produto" in df.columns:
            df["bloco_financiamento"] = df["tp_produto"].map(mapping).fillna("Não Identificado")
        return df

    @staticmethod
    def calculate_stock_coverage(df: pd.DataFrame, pop_data: pd.DataFrame = None):
        """
        Calcula a cobertura de estoque per capita.
        Essencial para identificar desigualdades regionais de acesso.
        """
        # Exemplo de lógica: Unidades de saúde por 100k habitantes
        coverage = (
            df.groupby(["sg_uf", "no_municipio"])
            .agg({"qt_estoque": "sum", "co_cnes": "nunique"})
            .rename(columns={"co_cnes": "pontos_distribuicao"})
        )

        return coverage.reset_index()

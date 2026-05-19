import pandas as pd
from .utils import logger

# Contrato Estrito de Dados (Data Contract)
# Garante que modelos de ML não recebam lixo
EXPECTED_SCHEMA = {
    'sg_uf': 'category',
    'co_municipio_ibge': 'int64',
    'no_municipio': 'string',
    'co_cnes': 'int64',
    'dt_posicao_estoque': 'datetime64[ns]',
    'co_catmat': 'category',
    'ds_produto': 'string',
    'qt_estoque': 'float64',
    'dt_validade': 'datetime64[ns]',
    'tp_produto': 'category'
}

# Mapeamento de Sinonímia (Resiliência a mudanças do governo)
COLUMN_ALIASES = {
    'nu_latitude': 'latitude',
    'nu_longitude': 'longitude',
    'co_municipio': 'co_municipio_ibge',
    'quantidade': 'qt_estoque',
    'dt_ciclo_bnafar': 'dt_posicao_estoque'
}

def detect_data_drift(df: pd.DataFrame):
    """Detecta se o governo introduziu colunas novas (oportunidade de dados)."""
    current_cols = set(df.columns)
    expected_cols = set(EXPECTED_SCHEMA.keys())
    new_cols = current_cols - expected_cols
    if new_cols:
        logger.info(f"DATA DRIFT: Detectadas novas colunas no portal: {new_cols}")
    return list(new_cols)

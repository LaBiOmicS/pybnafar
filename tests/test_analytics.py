import pytest
import pandas as pd
import numpy as np
from pybnafar.analytics import BnafarAnalytics

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'sg_uf': ['SP', 'SP', 'RJ', 'RJ'],
        'no_municipio': ['Mun A', 'Mun A', 'Mun B', 'Mun B'],
        'co_municipio_ibge': [1, 1, 2, 2],
        'co_catmat': ['101', '101', '101', '101'],
        'ds_produto': ['Prod A', 'Prod A', 'Prod A', 'Prod A'],
        'dt_ciclo_bnafar': pd.to_datetime(['2025-01-06', '2025-01-21', '2025-01-06', '2025-01-21']),
        'qt_estoque': [100, 0, 50, 40],
        'quinzena': [1, 2, 1, 2],
        'tp_produto': ['E', 'E', 'B', 'B'],
        'dias_para_vencer': [100, 90, 30, 20],
        'co_cnes': [1, 1, 2, 2]
    })

def test_detect_real_ruptures(sample_data):
    results = BnafarAnalytics.detect_real_ruptures(sample_data)
    rupturas = results['confirmed_ruptures']
    assert len(rupturas) == 1
    assert rupturas.iloc[0]['no_municipio'] == 'Mun A'

def test_calculate_priority_waste(sample_data):
    # Test with 30 days threshold
    ranking = BnafarAnalytics.calculate_priority_waste(sample_data, days=30)
    assert len(ranking) == 1
    assert ranking.iloc[0]['no_municipio'] == 'Mun B'

def test_confidence_score(sample_data):
    scores = BnafarAnalytics.calculate_confidence_score(sample_data)
    assert 'confidence_score' in scores.columns
    assert scores.iloc[0]['confidence_score'] > 0

import pytest
import pandas as pd
import json
from pybnafar.interop import BnafarInterop

def test_to_fhir_inventory():
    df = pd.DataFrame({
        'dt_posicao_estoque': [pd.Timestamp('2025-01-01')],
        'co_catmat': ['123'],
        'ds_produto': ['Medicamento'],
        'qt_estoque': [50.0],
        'sg_uf': ['SP'],
        'co_municipio_ibge': [12345]
    })
    
    fhir_json = BnafarInterop.to_fhir_inventory(df)
    data = json.loads(fhir_json)
    
    assert isinstance(data, list)
    assert data[0]['resourceType'] == 'InventoryReport'
    assert data[0]['item'][0]['quantity']['value'] == 50.0

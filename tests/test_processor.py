import pandas as pd
import pytest

from pybnafar.processor import BnafarProcessor


def test_clean_and_type():
    df_raw = pd.DataFrame(
        {
            "SG_UF": ["SP"],
            "QT_ESTOQUE": ["10,50"],
            "DT_VALIDADE": ["2025-12-31"],
            "CO_MUNICIPIO": [3550308],
            "CO_CATMAT": ["101"],
        }
    )

    clean = BnafarProcessor._clean_and_type(df_raw)

    assert clean["sg_uf"].iloc[0] == "SP"
    assert clean["qt_estoque"].iloc[0] == 10.5
    assert pd.api.types.is_datetime64_any_dtype(clean["dt_validade"])
    assert "co_municipio_ibge" in clean.columns


def test_process_corrupted_schema(tmp_path):
    # Test with a CSV that has missing mandatory columns
    csv_path = tmp_path / "corrupted.csv"
    pd.DataFrame({"wrong_col": [1, 2]}).to_csv(csv_path, index=False)

    # Processor should raise an error if columns are missing during cleaning
    with pytest.raises(KeyError):
        BnafarProcessor._clean_and_type(pd.read_csv(csv_path))

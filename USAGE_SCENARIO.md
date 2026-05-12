# Reproducible Usage Scenario: Pharmaceutical Shortage Detection

This scenario demonstrates how to use `pybnafar` to detect medicine stockouts (shortages) and export the data to HL7 FHIR for government reporting.

## 1. Environment Setup

### Option A: Local (Micromamba/Conda)
```bash
micromamba create -f environment.yml
micromamba activate pybnafar
pip install -e .
```

### Option B: Docker (Recommended for Servers)
```bash
docker build -t pybnafar .
docker run -p 8501:8501 -v $(pwd)/data:/app/bnafar_workspace pybnafar
```

## 2. Generate Mock Data (The "Bnafar-Real" simulation)
Create a file named `reproduce_case.csv`:
```csv
nu_cnpj;co_cnes;no_estabelecimento;no_municipio;co_municipio_ibge;sg_uf;tp_produto;co_catmat;ds_produto;qt_estoque;dt_posicao_estoque;dt_ciclo_bnafar
00000000000101;1234567;FARMACIA CENTRAL;BELO HORIZONTE;310620;MG;E;1001;INSULINA NPH;500;2026-05-01;2026-05-01
00000000000101;1234567;FARMACIA CENTRAL;BELO HORIZONTE;310620;MG;E;1001;INSULINA NPH;0;2026-05-15;2026-05-15
00000000000102;7654321;POSTO SAUDE;SAO PAULO;355030;SP;S;2002;AMOXICILINA 500MG;1000;2026-05-01;2026-05-01
```

## 3. Execution Pipeline

### Terminal Analysis (CLI)
Run the automated report:
```bash
# Process the mock data and show the intelligence report
export PYTHONPATH=.
python -c "from pybnafar.processor import BnafarProcessor; BnafarProcessor.process_and_partition('reproduce_case.csv', 'my_lake', 'my_manifests', {'snapshot': 'Reproduction'})"
pybnafar --report --workspace .
```

### Interactive Visualization
Launch the dashboard to explore the data visually:
```bash
pybnafar --dashboard
```

## 4. Expected Results
- **Stockout Detection**: The system should flag **INSULINA NPH** in **Belo Horizonte** as a confirmed rupture because the stock went from 500 to 0.
- **Data Confidence**: Belo Horizonte should receive a higher score than São Paulo due to the frequency of reports.
- **FHIR Export**: Clicking the export button in the dashboard should generate an RNDS-compliant JSON resource.

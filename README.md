# pybnafar 🇧🇷

[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)](https://github.com/LaBiOmicS/pybnafar)
[![FHIR R4](https://img.shields.io/badge/FHIR-R4%20compliant-green.svg)](https://hl7.org/fhir/R4/)

**pybnafar** is a high-performance Python SDK and clinical intelligence platform for the Brazilian **Base Nacional de Dados de Ações e Serviços da Assistência Farmacêutica (BNAFAR)**. It automates the extraction, cleaning, and analysis of pharmaceutical data from the SUS (Brazilian Unified Health System).

---

## 🛠️ Comprehensive Quick Start

### 1. Installation
Install directly via Pip (or use Micromamba/Docker):
```bash
pip install pybnafar
```

### 2. Full Pipeline Example
This script syncs data, loads it, and calculates critical health indicators.

```python
from pybnafar import Bnafar

# Initialize workspace (where your Data Lake will live)
bn = Bnafar(workspace='sus_intelligence')

# Step 1: Sync with OpenDATASUS (Downloads and processes millions of records)
bn.sync()

# Step 2: Load data for specific States (High performance using Hive pushdown)
df = bn.load_optimized(ufs=['MG', 'SP'])

# Step 3: Analytics - Detect Medicine Shortages (Ruptures)
results = bn.analytics.detect_real_ruptures(df)
confirmed_ruptures = results['confirmed_ruptures']
print(f"Shortages detected in: {confirmed_ruptures['no_municipio'].unique()}")

# Step 4: Ethical Audit - Data Confidence Index
confidence = bn.analytics.calculate_confidence_score(df)
print(confidence.head())

# Step 5: Interoperability - Export to RNDS (FHIR)
fhir_json = bn.interop.to_fhir_inventory(df.head(10))
with open("rnds_report.json", "w") as f:
    f.write(fhir_json)
```

---

## 🖥️ CLI Commands (Deep Dive)

The CLI allows full management without writing code:

- **`pybnafar --sync`**: Automates the bi-monthly update cycle. resiliant to network failures.
- **`pybnafar --dashboard`**: Launches the interactive **Streamlit** UI for visual exploration.
- **`pybnafar --report --ufs RJ`**: Prints a technical intelligence summary of the specified State.
- **`pybnafar --workspace /path/to/disk`**: Customizes storage location for Big Data environments.

---

## 🏗️ Architecture Best Practices

- **Atomic Writes**: Data is never corrupted; processing uses temporary buffers and manifest validation.
- **Ethical AI Ready**: Includes a **Data Confidence Index (DCI)** that prevents algorithm bias by flagging municipalities with infrastructure-related data gaps.
- **Interoperability**: Native HL7 FHIR R4 support for immediate integration with the Brazilian Health Data Network (RNDS).

---

## 📚 Resources
- [Full Technical Manual](docs/DOCUMENTATION.md)
- [Brazilian User Guide (PT-BR)](README_BR.md)
- [Reproducible Usage Scenario](USAGE_SCENARIO.md)
- [Contribution Guidelines](CONTRIBUTING.md)

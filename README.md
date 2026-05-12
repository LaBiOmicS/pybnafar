# pybnafar 🇧🇷

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FHIR R4](https://img.shields.io/badge/FHIR-R4%20compliant-green.svg)](https://hl7.org/fhir/R4/)

**pybnafar** is a high-performance Python SDK and clinical intelligence platform for the Brazilian **Base Nacional de Dados de Ações e Serviços da Assistência Farmacêutica (BNAFAR)**.

## 🚀 Key Features

- **Big Data Scalability**: Hive-partitioned Data Lake using Apache Arrow.
- **RNDS Interoperability**: Validated HL7 FHIR R4 JSON export for the Brazilian Health Data Network.
- **Clinical Intelligence**: Automated detection of shortages (stockouts) and waste risk.
- **Ethical Governance**: Built-in Data Confidence Index (DCI) to prevent algorithmic bias.
- **Ready for Production**: Native support for **Micromamba** and **Docker**.

## 🖥️ Usage

### Installation
```bash
pip install git+https://github.com/usuario/pybnafar.git
```

### CLI Operations
```bash
# Sync government data
pybnafar --sync

# Launch the interactive Dashboard
pybnafar --dashboard

# Generate intelligence report in terminal
pybnafar --report --ufs MG SP
```

### Docker (Quick Start)
```bash
docker build -t pybnafar .
docker run -p 8501:8501 -v $(pwd)/my_data:/app/bnafar_workspace pybnafar
```

## 📚 Documentation
- [Usage Scenario & Replication](USAGE_SCENARIO.md)
- [Technical Reference](docs/DOCUMENTATION.md)
- [Brazilian Managers Guide (PT-BR)](README_BR.md)

# Technical Documentation: pybnafar v2.1

## 1. Data Engineering Architecture

### Data Lake (Hive-Partitioned)
`pybnafar` implements a partitioned storage strategy using **Apache Arrow**.
- **Schema Enforcement**: All snapshots are normalized against `schema.py`.
- **Data Drift Detection**: The system logs whenever the Ministry of Health adds or changes columns in the source CSV.
- **Partitioning Strategy**: Data is partitioned by State (`sg_uf`) and Year-Month (`ano_mes`).

### Resilience & Atomic Writes
To prevent corruption, writes are performed in a `_processing_temp` directory. A manifest JSON file is generated for each snapshot, containing a SHA-256 hash of the original file for provenance tracking.

---

## 2. Clinical Intelligence (Analytics)

### Data Confidence Index (DCI)
A weighted metric (0.0 to 1.0) based on:
- **Reporting Frequency (40%)**: Consistency of monthly reports.
- **Network Coverage (40%)**: Ratio of active CNES establishments.
- **Recency (20%)**: Delay since the last update.

### Rupture Detection
Distinguishes between **Confirmed Stockouts** (stock quantity went to zero) and **Compliance Silence** (municipality failed to report).

---

## 3. Interoperability (RNDS/FHIR)

The library uses `fhir.resources` for strict R4 validation.
- **Resource**: `InventoryReport`.
- **Profiles**: Aligned with the Brazilian National Health Data Network (RNDS).
- **Terminology**: Uses `http://purl.org/obm/catmat` for medicine coding.

---

## 4. Deployment & Reproducibility

### Micromamba / Conda
We use `environment.yml` for isolated environment management, ensuring that C-extensions for PyArrow and Pandas are correctly linked.

### Docker
The containerized version runs the **Streamlit Dashboard** by default, mounting the workspace as a persistent volume to allow data persistence across container restarts.

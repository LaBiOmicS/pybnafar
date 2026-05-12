# Technical Reference Manual: pybnafar v2.1

`pybnafar` is a specialized SDK for the Brazilian National Pharmaceutical Database. This document details every module, class, and method available.

---

## 1. Core Module: `Bnafar`
The main entry point for the library.

### `Bnafar(workspace='bnafar_system')`
Initializes the environment and directory structure.
- **`workspace`** (str): The path to the directory where data will be stored. Defaults to `'bnafar_system'`. It will create subdirectories: `/raw`, `/lake_partitioned`, and `/manifests`.

### `sync(use_api=True)`
Synchronizes local storage with official OpenDATASUS snapshots.
- **`use_api`** (bool): If `True`, attempts to use the official CKAN API. If `False` or if the API fails, it falls back to web scraping.
- **Logic**: It identifies missing snapshots by comparing local manifests with remote resources, downloads them, and processes them into the Data Lake.

### `load_optimized(ufs=None, months=None)`
High-performance loading of the Data Lake using Hive-partition pushdown.
- **`ufs`** (List[str], optional): List of State initials (e.g., `['SP', 'MG']`). If `None`, loads all states.
- **`months`** (List[str], optional): List of Year-Month strings (format `YYYY-MM`). If `None`, loads all dates.
- **Returns**: `pd.DataFrame` containing the filtered dataset.

---

## 2. Analytics Module: `BnafarAnalytics`
Advanced mathematical functions for public health surveillance.

### `calculate_confidence_score(df)`
Generates the Data Confidence Index (DCI) for each municipality.
- **`df`** (pd.DataFrame): The input dataset.
- **Metrics (Weighted)**:
  - *Temporal Consistency (40%)*: Ratio of cycles reported vs. total cycles.
  - *Network Coverage (40%)*: Ratio of active CNES establishments in the last cycle vs. historical maximum.
  - *Recency (20%)*: Proximity of the last report to the current date.
- **Returns**: A DataFrame with `confidence_score`, `confidence_category` (Low, Medium, High), and metadata.

### `detect_real_ruptures(df)`
Distinguishes between actual medicine shortages and reporting failures.
- **`df`** (pd.DataFrame): The input dataset.
- **Logic**: Compares stock levels between the two most recent cycles.
- **Returns**: A Dictionary with:
  - `confirmed_ruptures`: Products where stock was > 0 and became 0.
  - `reporting_failures`: Products where stock was > 0 and is now missing (NaN).

### `calculate_priority_waste(df, days=90)`
Ranks stock at risk of expiration weighted by public health criticality.
- **`df`** (pd.DataFrame): The input dataset.
- **`days`** (int): Expiration window in days.
- **Criticality Weights**: High-cost Specialized meds (E) = 3; Strategic (S) = 2; Basic (B/O) = 1.
- **Returns**: A DataFrame sorted by a `severity_index`.

---

## 3. Interoperability: `BnafarInterop`
Standardizes data for international and national health networks.

### `to_fhir_inventory(df)`
Exports data to HL7 FHIR R4.
- **`df`** (pd.DataFrame): Data to export (usually filtered to a specific municipality).
- **Profile**: Compliant with RNDS (Rede Nacional de Dados de Saúde).
- **Format**: Returns a string (JSON-LD) containing a list of `InventoryReport` resources.

---

## 4. Diagnostics: `BnafarDiagnostics`
Ensures ethical and technical integrity.

### `check_geographic_bias(df)`
Identifies states or regions underrepresented in the dataset.
- **`df`** (pd.DataFrame): The input dataset.
- **Warning**: Automatically logs an ethical notice regarding infrastructure-driven bias.

### `validate_integrity(df)`
Detects logistical outliers.
- **`df`** (pd.DataFrame): The input dataset.
- **Threshold**: Flags any record with `qt_estoque` > 1,000,000 units.

---

## 5. Processor: `BnafarProcessor`
Low-level engine for data transformation.

### `process_and_partition(csv_path, output_dir, manifest_dir, metadata)`
Transforms raw CSV into Parquet.
- **`csv_path`** (str): Path to raw CSV.
- **`output_dir`** (str): Path to Data Lake.
- **`manifest_dir`** (str): Path to save metadata.
- **Features**: Schema enforcement, atomic writing (via temp dirs), and Hive partitioning.

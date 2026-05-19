---
title: 'pybnafar: A High-Performance Python SDK for Governance and Decision Support in the Brazilian National Pharmaceutical Database'
tags:
  - Python
  - Public Health Informatics
  - Pharmaceutical Assistance
  - Data Engineering
  - Evidence-Based Management
  - SUS
authors:
  - name: Fabiano Menegidio
    orcid: 0000-0002-3164-1627
    affiliation: 1
affiliations:
  - name: Independent Researcher / Health Informatics Specialist
    index: 1
date: 18 May 2026
bibliography: paper.bib
---

# Summary

The **Base Nacional de Dados de Ações e Serviços da Assistência Farmacêutica (BNAFAR)** is the central pillar of the Brazilian Unified Health System (SUS) for monitoring pharmaceutical supply chains. Updated bi-monthly by over 5,500 municipalities, it tracks the availability of essential medicines for 200 million citizens. However, the raw data provided via the OpenDATASUS portal presents significant technical barriers: massive volumes (millions of records per snapshot), inconsistent schemas, and lack of historical continuity.

`pybnafar` is a high-performance Python SDK designed to bridge the gap between raw public health data and actionable intelligence. It implements an automated, atomic data pipeline that transforms unstable CSV snapshots into a curated, Hive-partitioned Data Lake using `Pandas` [@pandas] and `PyArrow` [@pyarrow]. Beyond data engineering, the library embeds clinical and ethical intelligence through standardized metrics for stockout detection, waste risk assessment, and geographic bias auditing.

# Statement of Need

In Public Health Informatics, the "Garbage In, Garbage Out" (GIGO) principle is a critical threat to policy-making. Researchers often face "Data Silences"—periods or regions with missing data—that can lead to biased statistical models and flawed resource allocation. Existing workflows for BNAFAR data are largely manual, relying on spreadsheet software that fails to handle the dataset's scale or ensure provenance.

`pybnafar` addresses these challenges by providing:
1. **Infrastructure as Code for Health Data**: Automating the synchronization through official CKAN APIs and ensuring data integrity with SHA-256 hashing and atomic write transactions.
2. **Computational Scalability**: Utilizing **Apache Arrow** and **Hive-partitioning** to allow complex temporal analysis on consumer-grade hardware, democratizing access to Big Data for municipal managers.
3. **Clinical Governance**: Standardizing the calculation of **Stock Autonomy** and **Priority Waste Indices**, ensuring that different health secretariats use the same mathematical "yardstick" for efficiency.
4. **Bioethical Safeguards**: Implementing an automated **Data Confidence Index (DCI)** and geographic bias detection, forcing researchers to acknowledge data gaps before drawing conclusions that affect vulnerable populations.

# Architecture and Implementation

The library is organized into specialized modules:
- **`BnafarDownloader`**: Handles resilient network requests with automatic fallback mechanisms.
- **`BnafarProcessor`**: Executes "Schema Enforcement" and transforms data in memory-safe chunks.
- **`BnafarAnalytics`**: Provides vectorized mathematical functions for pharmaceutical surveillance.
- **`BnafarInterop`**: Exports data into **HL7 FHIR-compliant** [@hl7fhir] JSON-LD resources, aligning the SDK with international interoperability standards.

# Impact and Applications

`pybnafar` enables a wide range of applications, from academic research in Pharmacoepidemiology to the development of real-time dashboards for crisis management (e.g., detecting drug shortages during outbreaks). By reducing the time-to-insight from days to minutes, it empowers the SUS with a tool for sovereign and ethical data management.

# Acknowledgements

The author acknowledges the commitment of the Brazilian Ministry of Health to open data and the support of the biomedical engineering community in fostering open-source solutions for public health.

# References

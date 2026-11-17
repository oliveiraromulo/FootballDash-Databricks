# PaineldoFutebol - Databricks

This repository implements a football data pipeline built on Databricks, designed to collect, store, and refine information from an external sports API into a structured analytical model. The project follows a classic lakehouse pattern: raw ingestion, curated Bronze layer, and cleaned Silver layer, with local extraction scripts feeding Databricks volumes before being consumed by streaming tables.

## Project purpose

The main objective is to transform football data into reliable, query-ready datasets for analysis and future reporting. It organizes data around leagues, seasons, fixtures, and match metadata, preserving the original content first and then validating the useful fields for business use.

## Definition of principles

The project is guided by the following principles:

1. Raw-first ingestion
   - Data is first collected as close to the original source as possible.
   - The local extraction scripts pull raw JSON from the API and store it in Databricks volumes before any business transformation occurs.
   - This preserves fidelity and creates an auditable source of truth.

2. Clear layer separation
   - Bronze is the landing layer: it keeps the original data structure and metadata, such as file name and modification time.
   - Silver is the validated layer: it simplifies, filters, and enforces required fields for downstream use.
   - This makes the pipeline understandable, testable, and easier to evolve.

3. Data quality by design
   - Null and mandatory-field checks are part of the model.
   - The Silver layer defines expectations such as non-null season year and league identifier, preventing invalid records from reaching downstream consumers.
   - Data quality is treated as a first-class requirement, not an afterthought.

4. Reproducibility and environment awareness
   - Extraction and Databricks credentials are centralized in helper functions and configuration files.
   - The project expects environments to be clearly differentiated between local and production-like settings, which makes deployment and maintenance more predictable.

5. Traceability and operational visibility
   - Each file keeps metadata such as file path and modification time.
   - The pipeline records where the data came from and when it was loaded, improving debugging and lineage analysis.
   - Every extraction result can be traced back to a specific source response.

6. Simple and modular architecture
   - The repository separates responsibilities into meaningful areas: extraction scripts, Bronze definitions, Silver transformations, and shared utility functions.
   - This keeps each part small, readable, and focused on a single responsibility.

7. Analytical readiness
   - The final objective is not only storage, but producing curated data that can be consumed quickly for analysis, dashboards, and future data products.
   - Each layer is shaped to support practical use, not just technical ingestion.

## Repository structure

- 0 - local_extractions: scripts that fetch and package raw JSON from the external football API.
- 1 - bronze: streaming tables that ingest raw data files and retain metadata.
- 2 - silver: curated tables that enforce constraints and normalize the dataset for analytics.
- utils: shared functions for credentials, API access, and uploading files to Databricks volumes.

## Data flow

1. Local extraction scripts request data from the Football API.
2. The response is saved as JSON in a local utility folder and then uploaded to a Databricks volume.
3. Bronze tables read from the volume and preserve raw records plus file metadata.
4. Silver tables select, clean, and validate the necessary fields.
5. The curated dataset becomes the reliable base for analysis, reporting, and future transformations.

## Core mindset

This project follows a pragmatic data engineering standard: land raw data faithfully, standardize it carefully, validate it explicitly, and make it ready for analysis without losing source traceability.

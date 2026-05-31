# Azure Data Factory Artifacts

This folder contains Azure Data Factory artifacts for Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform.

## Main Pipeline

`pl_dev_project5_ingest_landing_to_raw`

## Pipeline Purpose

This pipeline validates Project 5 source files in the Azure Storage landing zone, copies valid files into the raw zone, and orchestrates Databricks notebooks for Bronze, Silver, and Gold processing.

## Pipeline Flow

```text
Landing Zone
    ↓
Get Metadata file checks
    ↓
If Condition: all required files exist
    ↓
Copy Data activities: landing to raw
    ↓
Databricks Notebook: Bronze ingestion
    ↓
Databricks Notebook: Silver customer intelligence
    ↓
Databricks Notebook: Gold business insights


Source Files Validated
customers.csv
products.csv
orders.csv
order_items.csv
payments.csv
shipments.csv
returns.csv
customer_reviews.csv
support_tickets.csv
chat_feedback.json
Linked Services
Azure Blob Storage

ls_p4_blob_europedata

Used by ADF to access the Azure Storage container:

project5-customer-feedback-platform

Azure Databricks

AzureDatabricks1

Used by ADF to trigger Project 5 Databricks notebooks.

Security Note

Real Azure Storage keys and Databricks tokens are not stored in this repository.

Secrets are replaced with placeholders such as:

<REPLACE_WITH_SECRET>
<REPLACE_WITH_DATABRICKS_TOKEN>
<REPLACE_WITH_CLUSTER_ID>

In production, credentials should be managed using:

Azure Key Vault
Databricks Secret Scope
Managed Identity
Service Principal authentication
Role-based access control
# Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform

## Project Overview

This project builds an AI-powered customer feedback and supply chain intelligence platform for an online retail business.

The platform combines order data, product data, payment data, shipment data, return data, customer reviews, support tickets, and chat feedback to identify customer pain points and supply chain risks.

## Business Objective

The objective of this project is to help the business answer questions such as:

- Which products receive the most positive customer feedback?
- Which products receive the most complaints?
- Which issues are related to delivery, payment, login, product quality, or returns?
- Which products are frequently recommended by customers?
- Which complaints may indicate supplier or supply chain problems?
- Which orders are affected by delivery delays, payment failures, or return issues?

## Technology Stack

- Azure Blob Storage / Data Lake style folder structure
- Azure Data Factory
- Azure Databricks
- PySpark
- Delta Lake
- Databricks Unity Catalog
- GitHub
- PyCharm

## Planned Architecture

```text
Source Files
    ↓
Azure Storage Landing Zone
    ↓
Azure Data Factory
    - File validation
    - Landing to raw copy
    ↓
Azure Storage Raw Zone
    ↓
Databricks Bronze Layer
    - Raw ingestion
    - Delta table creation
    ↓
Databricks Silver Layer
    - Data cleaning
    - Customer feedback classification
    - Sentiment labeling
    - Complaint category logic
    ↓
Databricks Gold Layer
    - Product feedback summary
    - Complaint summary
    - Delivery issue analysis
    - Payment and login issue analysis
    - Return reason analysis
    - Product recommendation ranking
    - Supply chain customer risk

Source Data

Planned source files:

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
Project Status
Phase	Status
Phase 1	Project setup and source data generation
Phase 2	Azure Data Factory ingestion
Phase 3	Databricks Bronze, Silver, Gold processing
Phase 4	ADF orchestration and GitHub documentation
Security Note

No real access keys, tokens, passwords, or secrets should be committed to this repository.

Production secrets should be managed using Azure Key Vault, Databricks Secret Scope, Managed Identity, or Service Principal authentication.
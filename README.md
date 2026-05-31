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


## Project Status

| Phase | Status |
|---|---|
| Phase 1 | Completed - Project setup, source data generation, profiling, GitHub setup, and Azure landing upload |
| Phase 2 | Completed - Azure Data Factory landing-to-raw ingestion pipeline |
| Phase 3 | Completed - Databricks Bronze, Silver, and Gold processing |
| Phase 4 | Completed - ADF orchestration of Databricks notebooks and GitHub-safe documentation |

## Current Completed Architecture

```text
Generated Source Files
    ↓
Azure Storage Landing Zone
    ↓
Azure Data Factory
    - Get Metadata file validation
    - If Condition control flow
    - Copy Data activities
    ↓
Azure Storage Raw Zone
    ↓
ADF triggers Databricks notebooks
    ↓
Bronze Delta Tables
    ↓
Silver Customer Intelligence Tables
    ↓
Gold Business Insight Tables
    ↓
Databricks Unity Catalog Validation


Completed Gold Tables
gold_product_feedback_summary
gold_customer_complaint_summary
gold_delivery_issue_analysis
gold_payment_login_issue_analysis
gold_return_reason_analysis
gold_product_recommendation_ranking
gold_customer_sentiment_trend
gold_supply_chain_customer_risk
Final Project Outcome

This project successfully demonstrates an end-to-end AI-style customer feedback and supply chain intelligence platform.

The platform processes structured and semi-structured data from orders, payments, shipments, returns, customer reviews, support tickets, and chat feedback.

The Silver layer classifies customer sentiment, complaint categories, payment/login issues, delivery issues, product quality concerns, and supply chain impact.

The Gold layer creates business-ready insight tables that can support reporting, analytics, and future AI/RAG use cases.
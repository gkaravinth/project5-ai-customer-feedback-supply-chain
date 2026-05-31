# Project 5 Architecture

## Project Name

Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform

## Important Scope Clarification

This project does not implement a full RAG system yet.

The current version implements customer feedback analytics using Azure Data Factory, Azure Databricks, PySpark, Delta Lake, and Unity Catalog.

Customer feedback is analyzed using rule-based PySpark classification logic.

RAG, Azure OpenAI, vector search, and document-based question answering are future enhancements.

## Business Scenario

An online retail company receives data from multiple operational and customer-facing systems.

The company wants to understand:

- Which products receive strong customer feedback
- Which products receive complaints
- Which customers are high risk because of complaints or negative feedback
- Which delivery issues affect customers
- Which payment or login issues affect order experience
- Which return reasons indicate product or supply chain problems
- Which products should be recommended based on reviews and ratings

## Source Data

The project uses the following source files:

- customers.csv
- products.csv
- orders.csv
- order_items.csv
- payments.csv
- shipments.csv
- returns.csv
- customer_reviews.csv
- support_tickets.csv
- chat_feedback.json

## Azure Storage Design

The Azure Storage container is:

```text
project5-customer-feedback-platform

The container uses the following folders:

landing/
raw/
processed/
archive/
rejected/

End-to-End Architecture

Generated Source Files
        ↓
Azure Storage Landing Zone
        ↓
Azure Data Factory
        - Get Metadata file checks
        - If Condition
        - Copy Data activities
        ↓
Azure Storage Raw Zone
        ↓
ADF Databricks Notebook Orchestration
        ↓
Bronze Layer
        - Raw Delta tables
        - Ingestion metadata
        ↓
Silver Layer
        - Cleaned data
        - Standardized data types
        - Invalid record filtering
        - Customer sentiment labeling
        - Complaint classification
        - Delivery issue flag
        - Payment/login issue flag
        - Supply chain impact flag
        ↓
Gold Layer
        - Business-ready insight tables
        ↓
Unity Catalog Validation

Databricks Medallion Architecture

Bronze Layer

Bronze stores raw data from the Azure Storage raw zone as Delta tables.

Silver Layer

Silver applies cleaning, filtering, standardization, and customer intelligence classification.

The Silver layer creates:

Sentiment labels
Review issue categories
Support ticket severity scores
Supply chain impact flags
Payment/login issue flags
Delivery issue flags
Chat sentiment labels
Gold Layer

Gold creates business-ready tables for reporting and analytics.

Completed Gold tables:

gold_product_feedback_summary
gold_customer_complaint_summary
gold_delivery_issue_analysis
gold_payment_login_issue_analysis
gold_return_reason_analysis
gold_product_recommendation_ranking
gold_customer_sentiment_trend
gold_supply_chain_customer_risk
ADF Orchestration Flow
Check landing files
        ↓
If all required files exist
        ↓
Copy landing files to raw
        ↓
Run Bronze notebook
        ↓
Run Silver notebook
        ↓
Run Gold notebook
Future Enhancements

Future versions can include:

Azure OpenAI
RAG-based customer support assistant
Vector search over support policies and product documents
Power BI dashboard
Real-time streaming using Event Hubs
CI/CD deployment
Azure Key Vault and managed identity integration
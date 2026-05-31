# Project 5 Video Presentation Script

## AI Customer Feedback & Supply Chain Intelligence Platform

Hi everyone, my name is Aravinth.

Today I am going to present my Project 5, called **AI Customer Feedback and Supply Chain Intelligence Platform**.

This is a cloud data engineering project built using **Azure Blob Storage, Azure Data Factory, Azure Databricks, PySpark, Delta Lake, Databricks Unity Catalog, GitHub, and rule-based customer feedback classification**.

The main purpose of this project is to connect customer experience data with supply chain intelligence.

In real e-commerce businesses, customer complaints, product reviews, return reasons, payment issues, login issues, and delivery problems all contain valuable signals. If these signals are properly processed, the business can identify product quality issues, supplier-related risks, delivery problems, and customer satisfaction trends earlier.

---

## Business Scenario

For this project, I created a fictional online retail business.

The business sells products through an online channel and receives different types of customer and operational data.

The company receives:

* Customer orders
* Order item details
* Payment records
* Shipment records
* Return records
* Customer reviews
* Support tickets
* Chat feedback

The business wants to answer important questions such as:

* Which products receive the best customer feedback?
* Which products receive the most complaints?
* Which customers are at high complaint risk?
* Which delivery issues are affecting customers?
* Which payment or login issues are causing customer friction?
* Which return reasons indicate product or supply chain problems?
* Which products are highly recommended by customers?
* Which products create customer-facing supply chain risk?

This is the business problem I solved in this project.

---

## Important Scope Clarification

This project does **not** implement a full RAG system yet.

The current version uses **rule-based PySpark classification** to analyze customer feedback, support tickets, reviews, and chat topics.

RAG, Azure OpenAI, vector search, and policy-based question answering are planned as future enhancements.

So the current completed project is a **customer feedback analytics and supply chain intelligence platform**, not a full RAG application.

---

## Source Data

I generated realistic sample source files using Python.

The source files include:

* customers.csv
* products.csv
* orders.csv
* order_items.csv
* payments.csv
* shipments.csv
* returns.csv
* customer_reviews.csv
* support_tickets.csv
* chat_feedback.json

The CSV files represent structured data such as customers, products, orders, payments, shipments, returns, reviews, and support tickets.

The JSON file represents semi-structured chat feedback data, including customer information, chat topic, satisfaction score, and nested chat messages.

I also included some intentionally invalid records to test cleaning and validation logic in the Silver layer.

---

## Azure Storage Layer

After generating the data, I uploaded the source files into Azure Blob Storage using a data lake style folder structure.

The Azure container used for this project is:

**project5-customer-feedback-platform**

The container includes these folders:

* landing
* raw
* processed
* archive
* rejected

The **landing** folder stores the original uploaded source files.

The **raw** folder stores validated files copied by Azure Data Factory.

The other folders are included to represent production-style lake design.

---

## Azure Data Factory Ingestion

Next, I created an Azure Data Factory pipeline.

The pipeline first validates whether all required source files exist in the landing zone.

I used **Get Metadata** activities to check file existence for all 10 source files.

Then I used an **If Condition** activity to check whether all required files are available.

If all files exist, the pipeline runs Copy Data activities and moves files from the landing zone to the raw zone.

This gives us a controlled ingestion process:

Landing zone
to file validation
to raw zone.

After this, I extended the pipeline to orchestrate Databricks notebooks.

The final ADF pipeline runs:

* Landing file validation
* Landing to raw copy
* Bronze Databricks notebook
* Silver Databricks notebook
* Gold Databricks notebook

This means Azure Data Factory controls the full data engineering workflow.

---

## Databricks Bronze Layer

After the raw files are ready, ADF triggers the Bronze notebook in Azure Databricks.

The Bronze layer reads raw CSV and JSON files from Azure Storage and writes them as Delta tables.

The Bronze tables include:

* bronze_customers
* bronze_products
* bronze_orders
* bronze_order_items
* bronze_payments
* bronze_shipments
* bronze_returns
* bronze_customer_reviews
* bronze_support_tickets
* bronze_chat_feedback_raw

The Bronze layer keeps the data mostly as-is.

I also added ingestion metadata such as:

* ingestion timestamp
* source file path

This helps with auditability, debugging, and future reprocessing.

---

## Databricks Silver Layer

After Bronze completes, ADF triggers the Silver notebook.

The Silver layer cleans, filters, standardizes, and classifies the data.

In the Silver layer, I performed:

* Data type casting
* Date conversion
* Duplicate removal
* Invalid record filtering
* Currency validation
* Payment issue flagging
* Delivery delay calculation
* Delivery issue classification
* Return issue classification
* Review sentiment classification
* Support ticket severity scoring
* Chat feedback classification

For example, customer review sentiment is classified using the rating:

* Rating 4 or 5 is Positive
* Rating 3 is Neutral
* Rating 1 or 2 is Negative

Support tickets are classified using priority:

* Critical = severity score 4
* High = severity score 3
* Medium = severity score 2
* Low = severity score 1

I also created flags for:

* Payment issues
* Login issues
* Delivery issues
* Product quality issues
* Supply chain impact

This Silver layer converts raw operational and customer data into trusted customer intelligence data.

---

## Databricks Gold Layer

After Silver completes, ADF triggers the Gold notebook.

The Gold layer creates business-ready insight tables.

The completed Gold tables are:

* gold_product_feedback_summary
* gold_customer_complaint_summary
* gold_delivery_issue_analysis
* gold_payment_login_issue_analysis
* gold_return_reason_analysis
* gold_product_recommendation_ranking
* gold_customer_sentiment_trend
* gold_supply_chain_customer_risk

These Gold tables are designed for analytics and reporting.

For example, the product feedback summary table shows total reviews, average rating, positive reviews, negative reviews, and recommendation percentage by product.

The customer complaint summary table identifies customers with high complaint risk based on critical tickets, high-priority tickets, negative reviews, and negative chat feedback.

The delivery issue analysis table helps identify delivery problems by country, carrier, and delivery status.

The supply chain customer risk table identifies products with high return counts and negative review counts, which may indicate supplier, quality, or fulfillment problems.

---

## Unity Catalog Validation

After creating Bronze, Silver, and Gold tables, I validated the tables in Databricks Unity Catalog.

The schemas created are:

* project5_bronze
* project5_silver
* project5_gold

I confirmed that all Bronze, Silver, and Gold tables were created successfully.

I also created SQL validation queries and KPI queries to check table counts, data quality rules, sentiment distribution, issue categories, customer risk levels, and supply chain risk levels.

---

## GitHub and Documentation

I used GitHub for version control.

The repository includes:

* Source data generation scripts
* Source data profiling script
* Generated sample source files
* Azure Data Factory pipeline artifacts
* Databricks notebooks
* Architecture documentation
* Business rules
* Data dictionary
* SQL validation queries
* KPI queries
* Git workflow documentation
* README documentation

I also ensured that real storage keys and Databricks tokens were removed before pushing to GitHub.

Secrets were replaced with placeholders.

In production, secrets should be handled using:

* Azure Key Vault
* Databricks Secret Scope
* Managed Identity
* Service Principal authentication
* Role-based access control

---

## Key Business Outputs

This project creates business value by helping the company understand customer and supply chain issues.

The final Gold layer supports:

* Product feedback analysis
* Product recommendation ranking
* Customer complaint risk analysis
* Delivery issue analysis
* Payment and login issue analysis
* Return reason analysis
* Customer sentiment trend analysis
* Supply chain customer risk analysis

For example, if a product has many negative reviews and many supply chain-related returns, the business can investigate product quality, supplier performance, or fulfillment issues.

If delivery complaints are high for a specific carrier or country, the logistics team can investigate carrier performance.

If payment failures are high, the e-commerce team can review checkout experience and payment gateway issues.

This connects customer feedback directly to operational and supply chain decision-making.

---

## Key Learnings

Through this project, I practiced:

* Azure Storage data lake folder design
* Azure Data Factory file validation
* Get Metadata activities
* If Condition control flow
* Copy Data activities
* ADF orchestration of Databricks notebooks
* Databricks Bronze, Silver, and Gold architecture
* PySpark data cleaning
* Rule-based text and issue classification
* Delta Lake table creation
* Unity Catalog validation
* SQL validation and KPI queries
* GitHub version control
* Secret handling
* Cluster cost control

This project helped me understand how customer experience data can be processed and converted into supply chain intelligence.

---

## Future Enhancements

The next version of this project can include a full RAG system.

Future RAG implementation can use:

* Return policy documents
* Refund policy documents
* Delivery policy documents
* Product warranty documents
* Customer support SOP documents
* Supplier escalation SOP documents

These documents can be indexed using vector search and connected to Azure OpenAI.

Then business users or support agents can ask questions such as:

* What is the correct action for delayed delivery complaints?
* Which return policy applies for damaged products?
* Which supplier should be investigated based on customer complaints?
* What are the top customer issues this week?

This would turn the current analytics platform into an AI-powered customer support and supply chain assistant.

---

## Final Summary

To summarize, Project 5 is an end-to-end customer feedback and supply chain intelligence platform.

The pipeline starts with generated source data.

The data is uploaded to Azure Storage landing zone.

Azure Data Factory validates the files and copies them to the raw zone.

ADF then triggers Databricks notebooks to create Bronze, Silver, and Gold Delta tables.

The Silver layer applies customer feedback classification, sentiment labeling, issue categorization, and supply chain impact logic.

The Gold layer creates business-ready insight tables for analytics.

The project is validated in Databricks Unity Catalog and documented in GitHub.

This project demonstrates my hands-on skills in Azure Data Factory, Azure Databricks, PySpark, Delta Lake, Unity Catalog, GitHub, and customer intelligence data engineering.

Thank you.


Short LinkedIn caption

I completed Project 5: AI Customer Feedback & Supply Chain Intelligence Platform.

This project connects customer experience data with supply chain intelligence using Azure Blob Storage, Azure Data Factory, Azure Databricks, PySpark, Delta Lake, Unity Catalog, and GitHub.

The pipeline processes orders, payments, shipments, returns, customer reviews, support tickets, and chat feedback. It creates Bronze, Silver, and Gold Delta tables, with Silver-level rule-based classification for sentiment, delivery issues, payment/login issues, product quality concerns, and supply chain impact.

The Gold layer produces business-ready insight tables for product feedback, customer complaint risk, delivery issues, payment/login issues, return reasons, product recommendations, sentiment trends, and supply chain customer risk.

RAG is planned as a future enhancement, but the current project successfully demonstrates customer feedback analytics and supply chain intelligence using cloud data engineering.

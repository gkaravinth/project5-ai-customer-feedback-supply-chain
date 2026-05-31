# Databricks notebook source
# Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform
# Notebook: 00_config
# Purpose: Common configuration for storage paths, schemas, and table names

# COMMAND ----------

# ============================================================
# 1. Azure Storage configuration
# ============================================================

storage_account_name = "europedata"
container_name = "project5-customer-feedback-platform"

# IMPORTANT:
# Temporarily paste your real Azure Storage Account Key below only for execution.
# After successful run, replace it again with the placeholder before GitHub/export.
storage_account_key = "PLACE THE KEY HERE"

spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net",
    storage_account_key
)

print("Azure Storage access key configured for Databricks session.")

# COMMAND ----------

# ============================================================
# 2. Data lake paths
# ============================================================

base_path = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net"

landing_base_path = f"{base_path}/landing"
raw_base_path = f"{base_path}/raw"
processed_base_path = f"{base_path}/processed"

raw_customers_path = f"{raw_base_path}/customers.csv"
raw_products_path = f"{raw_base_path}/products.csv"
raw_orders_path = f"{raw_base_path}/orders.csv"
raw_order_items_path = f"{raw_base_path}/order_items.csv"
raw_payments_path = f"{raw_base_path}/payments.csv"
raw_shipments_path = f"{raw_base_path}/shipments.csv"
raw_returns_path = f"{raw_base_path}/returns.csv"
raw_customer_reviews_path = f"{raw_base_path}/customer_reviews.csv"
raw_support_tickets_path = f"{raw_base_path}/support_tickets.csv"
raw_chat_feedback_path = f"{raw_base_path}/chat_feedback.json"

print(f"Raw base path: {raw_base_path}")

# COMMAND ----------

# ============================================================
# 3. Unity Catalog / schema configuration
# ============================================================

catalog_name = "supplyspark"

bronze_database = f"{catalog_name}.project5_bronze"
silver_database = f"{catalog_name}.project5_silver"
gold_database = f"{catalog_name}.project5_gold"

print(f"Bronze database: {bronze_database}")
print(f"Silver database: {silver_database}")
print(f"Gold database: {gold_database}")

# COMMAND ----------

# ============================================================
# 4. Bronze table names
# ============================================================

bronze_customers_table = f"{bronze_database}.bronze_customers"
bronze_products_table = f"{bronze_database}.bronze_products"
bronze_orders_table = f"{bronze_database}.bronze_orders"
bronze_order_items_table = f"{bronze_database}.bronze_order_items"
bronze_payments_table = f"{bronze_database}.bronze_payments"
bronze_shipments_table = f"{bronze_database}.bronze_shipments"
bronze_returns_table = f"{bronze_database}.bronze_returns"
bronze_customer_reviews_table = f"{bronze_database}.bronze_customer_reviews"
bronze_support_tickets_table = f"{bronze_database}.bronze_support_tickets"
bronze_chat_feedback_table = f"{bronze_database}.bronze_chat_feedback_raw"

# COMMAND ----------

# ============================================================
# 5. Silver table names
# ============================================================

silver_customers_table = f"{silver_database}.silver_customers"
silver_products_table = f"{silver_database}.silver_products"
silver_orders_table = f"{silver_database}.silver_orders"
silver_order_items_table = f"{silver_database}.silver_order_items"
silver_payments_table = f"{silver_database}.silver_payments"
silver_shipments_table = f"{silver_database}.silver_shipments"
silver_returns_table = f"{silver_database}.silver_returns"
silver_customer_reviews_table = f"{silver_database}.silver_customer_reviews"
silver_support_tickets_table = f"{silver_database}.silver_support_tickets"
silver_chat_feedback_table = f"{silver_database}.silver_chat_feedback"
silver_chat_messages_table = f"{silver_database}.silver_chat_messages"

# COMMAND ----------

# ============================================================
# 6. Gold table names
# ============================================================

gold_product_feedback_summary_table = f"{gold_database}.gold_product_feedback_summary"
gold_customer_complaint_summary_table = f"{gold_database}.gold_customer_complaint_summary"
gold_delivery_issue_analysis_table = f"{gold_database}.gold_delivery_issue_analysis"
gold_payment_login_issue_analysis_table = f"{gold_database}.gold_payment_login_issue_analysis"
gold_return_reason_analysis_table = f"{gold_database}.gold_return_reason_analysis"
gold_product_recommendation_ranking_table = f"{gold_database}.gold_product_recommendation_ranking"
gold_customer_sentiment_trend_table = f"{gold_database}.gold_customer_sentiment_trend"
gold_supply_chain_customer_risk_table = f"{gold_database}.gold_supply_chain_customer_risk"

# COMMAND ----------

print("Project 5 configuration loaded successfully.")
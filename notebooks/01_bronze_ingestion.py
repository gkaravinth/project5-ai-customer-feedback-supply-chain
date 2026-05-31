#run in separate cell (1st cell)
%run ./00_config

#run in separate cell (2nd cell)
from pyspark.sql.functions import current_timestamp, lit

# Databricks notebook source
# Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform
# Notebook: 01_bronze_ingestion
# Purpose: Read raw source files from Azure Storage and write Bronze Delta tables




# COMMAND ----------

# Create Bronze schema/database if it does not exist
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {bronze_database}")

print(f"Bronze database ready: {bronze_database}")

# COMMAND ----------

def read_csv_from_raw(file_path):
    """
    Read CSV file from raw zone.
    Bronze layer keeps source data mostly as-is.
    """
    return (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(file_path)
        .withColumn("ingestion_timestamp", current_timestamp())
        .withColumn("source_file_path", lit(file_path))
    )


def read_json_from_raw(file_path):
    """
    Read nested JSON file from raw zone.
    Bronze layer keeps nested JSON structure mostly as-is.
    """
    return (
        spark.read
        .option("multiline", "true")
        .json(file_path)
        .withColumn("ingestion_timestamp", current_timestamp())
        .withColumn("source_file_path", lit(file_path))
    )


def write_bronze_table(df, table_name):
    """
    Write DataFrame as Delta table in Bronze database.
    Overwrite mode is acceptable for this development/training project.
    """
    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )

    row_count = df.count()
    print(f"Written table: {table_name} | Rows: {row_count}")
    return row_count

# COMMAND ----------

# Read raw CSV files
df_customers = read_csv_from_raw(raw_customers_path)
df_products = read_csv_from_raw(raw_products_path)
df_orders = read_csv_from_raw(raw_orders_path)
df_order_items = read_csv_from_raw(raw_order_items_path)
df_payments = read_csv_from_raw(raw_payments_path)
df_shipments = read_csv_from_raw(raw_shipments_path)
df_returns = read_csv_from_raw(raw_returns_path)
df_customer_reviews = read_csv_from_raw(raw_customer_reviews_path)
df_support_tickets = read_csv_from_raw(raw_support_tickets_path)

# Read raw JSON file
df_chat_feedback = read_json_from_raw(raw_chat_feedback_path)

print("All raw files read successfully.")

# COMMAND ----------

# Display raw row counts before Bronze write
print("Raw row counts before Bronze write:")
print(f"customers: {df_customers.count()}")
print(f"products: {df_products.count()}")
print(f"orders: {df_orders.count()}")
print(f"order_items: {df_order_items.count()}")
print(f"payments: {df_payments.count()}")
print(f"shipments: {df_shipments.count()}")
print(f"returns: {df_returns.count()}")
print(f"customer_reviews: {df_customer_reviews.count()}")
print(f"support_tickets: {df_support_tickets.count()}")
print(f"chat_feedback: {df_chat_feedback.count()}")

# COMMAND ----------

# Write Bronze Delta tables
row_counts = {}

row_counts["bronze_customers"] = write_bronze_table(df_customers, bronze_customers_table)
row_counts["bronze_products"] = write_bronze_table(df_products, bronze_products_table)
row_counts["bronze_orders"] = write_bronze_table(df_orders, bronze_orders_table)
row_counts["bronze_order_items"] = write_bronze_table(df_order_items, bronze_order_items_table)
row_counts["bronze_payments"] = write_bronze_table(df_payments, bronze_payments_table)
row_counts["bronze_shipments"] = write_bronze_table(df_shipments, bronze_shipments_table)
row_counts["bronze_returns"] = write_bronze_table(df_returns, bronze_returns_table)
row_counts["bronze_customer_reviews"] = write_bronze_table(df_customer_reviews, bronze_customer_reviews_table)
row_counts["bronze_support_tickets"] = write_bronze_table(df_support_tickets, bronze_support_tickets_table)
row_counts["bronze_chat_feedback_raw"] = write_bronze_table(df_chat_feedback, bronze_chat_feedback_table)

print("All Bronze tables created successfully.")

# COMMAND ----------

# Display Bronze row count validation summary
print("Bronze row count validation summary:")

for table_name, count_value in row_counts.items():
    print(f"{table_name}: {count_value}")

# COMMAND ----------

# Quick table check
spark.sql(f"SHOW TABLES IN {bronze_database}").show(truncate=False)

# COMMAND ----------

# Sample checks
print("Sample customers:")
spark.sql(f"SELECT * FROM {bronze_customers_table} LIMIT 5").show(truncate=False)

print("Sample customer reviews:")
spark.sql(f"SELECT * FROM {bronze_customer_reviews_table} LIMIT 5").show(truncate=False)

print("Sample chat feedback raw:")
spark.sql(f"SELECT chat_id, order_id, topic, satisfaction_score FROM {bronze_chat_feedback_table} LIMIT 5").show(truncate=False)

# COMMAND ----------

print("Project 5 Bronze ingestion completed successfully.")


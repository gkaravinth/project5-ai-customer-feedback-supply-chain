#run in separate cell (1st cell)
%run ./00_config


#run in separate cell (2nd cell)
# Databricks notebook source
# Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform
# Notebook: 02_silver_customer_intelligence
# Purpose: Clean Bronze data and create Silver customer intelligence tables

# COMMAND ----------

from pyspark.sql.functions import (
    col,
    trim,
    lower,
    upper,
    when,
    lit,
    to_date,
    to_timestamp,
    datediff,
    current_date,
    explode_outer,
    size,
    round as spark_round
)

# COMMAND ----------

# Create Silver schema/database if it does not exist
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {silver_database}")

print(f"Silver database ready: {silver_database}")

# COMMAND ----------

def write_silver_table(df, table_name):
    """
    Write DataFrame as Delta table in Silver database.
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

# Load Bronze tables
df_customers = spark.table(bronze_customers_table)
df_products = spark.table(bronze_products_table)
df_orders = spark.table(bronze_orders_table)
df_order_items = spark.table(bronze_order_items_table)
df_payments = spark.table(bronze_payments_table)
df_shipments = spark.table(bronze_shipments_table)
df_returns = spark.table(bronze_returns_table)
df_customer_reviews = spark.table(bronze_customer_reviews_table)
df_support_tickets = spark.table(bronze_support_tickets_table)
df_chat_feedback = spark.table(bronze_chat_feedback_table)

print("All Bronze tables loaded successfully.")

# COMMAND ----------

# ============================================================
# Customers Silver
# ============================================================

silver_customers = (
    df_customers
    .select(
        trim(col("CustomerID")).alias("CustomerID"),
        trim(col("CustomerName")).alias("CustomerName"),
        lower(trim(col("Email"))).alias("Email"),
        trim(col("Country")).alias("Country"),
        trim(col("City")).alias("City"),
        to_date(col("SignupDate")).alias("SignupDate"),
        trim(col("CustomerSegment")).alias("CustomerSegment"),
        col("IsActive").cast("boolean").alias("IsActive"),
        col("ingestion_timestamp"),
        col("source_file_path")
    )
    .filter(col("CustomerID").isNotNull())
    .filter(col("CustomerID") != "")
    .dropDuplicates(["CustomerID"])
)

# COMMAND ----------

# ============================================================
# Products Silver
# ============================================================

silver_products = (
    df_products
    .select(
        trim(col("ProductID")).alias("ProductID"),
        trim(col("SKU")).alias("SKU"),
        trim(col("ProductName")).alias("ProductName"),
        trim(col("Category")).alias("Category"),
        trim(col("SubCategory")).alias("SubCategory"),
        trim(col("Brand")).alias("Brand"),
        trim(col("SupplierID")).alias("SupplierID"),
        col("UnitCost").cast("double").alias("UnitCost"),
        col("RetailPrice").cast("double").alias("RetailPrice"),
        upper(trim(col("Currency"))).alias("Currency"),
        col("IsActive").cast("boolean").alias("IsActive"),
        col("ingestion_timestamp"),
        col("source_file_path")
    )
    .filter(col("ProductID").isNotNull())
    .filter(col("ProductID") != "")
    .filter(col("UnitCost") >= 0)
    .filter(col("RetailPrice") >= 0)
    .filter(col("Currency") == "EUR")
    .dropDuplicates(["ProductID"])
)

# COMMAND ----------

# ============================================================
# Orders Silver
# ============================================================

silver_orders = (
    df_orders
    .select(
        trim(col("OrderID")).alias("OrderID"),
        trim(col("CustomerID")).alias("CustomerID"),
        to_timestamp(col("OrderDate")).alias("OrderDate"),
        trim(col("OrderStatus")).alias("OrderStatus"),
        trim(col("SalesChannel")).alias("SalesChannel"),
        col("GrossAmount").cast("double").alias("GrossAmount"),
        col("DiscountAmount").cast("double").alias("DiscountAmount"),
        col("NetAmount").cast("double").alias("NetAmount"),
        upper(trim(col("Currency"))).alias("Currency"),
        col("ingestion_timestamp"),
        col("source_file_path")
    )
    .filter(col("OrderID").isNotNull())
    .filter(col("OrderID") != "")
    .filter(col("CustomerID").isNotNull())
    .filter(col("GrossAmount") >= 0)
    .filter(col("DiscountAmount") >= 0)
    .filter(col("NetAmount") >= 0)
    .filter(col("Currency") == "EUR")
    .filter(col("OrderStatus").isin("Completed", "Shipped", "Cancelled", "Returned"))
    .dropDuplicates(["OrderID"])
)

# COMMAND ----------

# ============================================================
# Order Items Silver
# ============================================================

silver_order_items = (
    df_order_items
    .select(
        trim(col("OrderItemID")).alias("OrderItemID"),
        trim(col("OrderID")).alias("OrderID"),
        trim(col("ProductID")).alias("ProductID"),
        col("Quantity").cast("int").alias("Quantity"),
        col("UnitPrice").cast("double").alias("UnitPrice"),
        col("LineTotal").cast("double").alias("LineTotal"),
        col("ingestion_timestamp"),
        col("source_file_path")
    )
    .filter(col("OrderItemID").isNotNull())
    .filter(col("OrderItemID") != "")
    .filter(col("OrderID").isNotNull())
    .filter(col("ProductID").isNotNull())
    .filter(col("Quantity") > 0)
    .filter(col("UnitPrice") >= 0)
    .filter(col("LineTotal") >= 0)
    .dropDuplicates(["OrderItemID"])
)

# COMMAND ----------

# ============================================================
# Payments Silver
# ============================================================

silver_payments = (
    df_payments
    .select(
        trim(col("PaymentID")).alias("PaymentID"),
        trim(col("OrderID")).alias("OrderID"),
        to_timestamp(col("PaymentDate")).alias("PaymentDate"),
        trim(col("PaymentMethod")).alias("PaymentMethod"),
        trim(col("PaymentStatus")).alias("PaymentStatus"),
        trim(col("PaymentFailureReason")).alias("PaymentFailureReason"),
        col("Amount").cast("double").alias("Amount"),
        upper(trim(col("Currency"))).alias("Currency"),
        col("ingestion_timestamp"),
        col("source_file_path")
    )
    .filter(col("PaymentID").isNotNull())
    .filter(col("PaymentID") != "")
    .filter(col("OrderID").isNotNull())
    .filter(col("Amount") >= 0)
    .filter(col("Currency") == "EUR")
    .filter(col("PaymentStatus").isin("Paid", "Failed", "Pending", "Refunded"))
    .withColumn(
        "PaymentIssueFlag",
        when(col("PaymentStatus") == "Failed", lit(1)).otherwise(lit(0))
    )
    .dropDuplicates(["PaymentID"])
)

# COMMAND ----------

# ============================================================
# Shipments Silver
# ============================================================

silver_shipments = (
    df_shipments
    .select(
        trim(col("ShipmentID")).alias("ShipmentID"),
        trim(col("OrderID")).alias("OrderID"),
        trim(col("WarehouseID")).alias("WarehouseID"),
        trim(col("Carrier")).alias("Carrier"),
        to_date(col("ShipmentDate")).alias("ShipmentDate"),
        to_date(col("ExpectedDeliveryDate")).alias("ExpectedDeliveryDate"),
        to_date(col("ActualDeliveryDate")).alias("ActualDeliveryDate"),
        trim(col("DeliveryStatus")).alias("DeliveryStatus"),
        trim(col("DeliveryCountry")).alias("DeliveryCountry"),
        col("ingestion_timestamp"),
        col("source_file_path")
    )
    .filter(col("ShipmentID").isNotNull())
    .filter(col("ShipmentID") != "")
    .filter(col("OrderID").isNotNull())
    .filter(col("DeliveryStatus").isin("Delivered", "In Transit", "Delayed", "Lost"))
    .withColumn(
        "DeliveryDelayDays",
        when(
            col("ActualDeliveryDate").isNotNull(),
            datediff(col("ActualDeliveryDate"), col("ExpectedDeliveryDate"))
        ).otherwise(lit(None))
    )
    .withColumn(
        "DeliveryIssueFlag",
        when(col("DeliveryStatus").isin("Delayed", "Lost"), lit(1))
        .when(col("DeliveryDelayDays") > 0, lit(1))
        .otherwise(lit(0))
    )
    .dropDuplicates(["ShipmentID"])
)

# COMMAND ----------

# ============================================================
# Returns Silver
# ============================================================

silver_returns = (
    df_returns
    .select(
        trim(col("ReturnID")).alias("ReturnID"),
        trim(col("OrderID")).alias("OrderID"),
        trim(col("ProductID")).alias("ProductID"),
        to_date(col("ReturnDate")).alias("ReturnDate"),
        col("ReturnQty").cast("int").alias("ReturnQty"),
        trim(col("ReturnReason")).alias("ReturnReason"),
        col("RefundAmount").cast("double").alias("RefundAmount"),
        col("ingestion_timestamp"),
        col("source_file_path")
    )
    .filter(col("ReturnID").isNotNull())
    .filter(col("ReturnID") != "")
    .filter(col("OrderID").isNotNull())
    .filter(col("ProductID").isNotNull())
    .filter(col("ReturnQty") > 0)
    .filter(col("RefundAmount") >= 0)
    .filter(col("ReturnReason").isNotNull())
    .filter(col("ReturnReason") != "")
    .withColumn(
        "SupplyChainReturnFlag",
        when(lower(col("ReturnReason")).contains("damaged"), lit(1))
        .when(lower(col("ReturnReason")).contains("wrong item"), lit(1))
        .when(lower(col("ReturnReason")).contains("quality"), lit(1))
        .when(lower(col("ReturnReason")).contains("late delivery"), lit(1))
        .otherwise(lit(0))
    )
    .dropDuplicates(["ReturnID"])
)

# COMMAND ----------

# ============================================================
# Customer Reviews Silver with sentiment classification
# ============================================================

silver_customer_reviews = (
    df_customer_reviews
    .select(
        trim(col("ReviewID")).alias("ReviewID"),
        trim(col("OrderID")).alias("OrderID"),
        trim(col("CustomerID")).alias("CustomerID"),
        trim(col("ProductID")).alias("ProductID"),
        to_date(col("ReviewDate")).alias("ReviewDate"),
        col("Rating").cast("int").alias("Rating"),
        trim(col("ReviewText")).alias("ReviewText"),
        col("RecommendationFlag").cast("boolean").alias("RecommendationFlag"),
        col("ingestion_timestamp"),
        col("source_file_path")
    )
    .filter(col("ReviewID").isNotNull())
    .filter(col("ReviewID") != "")
    .filter(col("OrderID").isNotNull())
    .filter(col("CustomerID").isNotNull())
    .filter(col("ProductID").isNotNull())
    .filter((col("Rating") >= 1) & (col("Rating") <= 5))
    .filter(col("ReviewText").isNotNull())
    .filter(col("ReviewText") != "")
    .withColumn(
        "SentimentLabel",
        when(col("Rating") >= 4, lit("Positive"))
        .when(col("Rating") == 3, lit("Neutral"))
        .otherwise(lit("Negative"))
    )
    .withColumn(
        "ReviewIssueCategory",
        when(lower(col("ReviewText")).contains("delivery"), lit("Delivery Issue"))
        .when(lower(col("ReviewText")).contains("payment"), lit("Payment Issue"))
        .when(lower(col("ReviewText")).contains("damaged"), lit("Product Quality Issue"))
        .when(lower(col("ReviewText")).contains("wrong item"), lit("Wrong Item"))
        .when(lower(col("ReviewText")).contains("quality"), lit("Product Quality Issue"))
        .when(lower(col("ReviewText")).contains("size"), lit("Size/Fit Issue"))
        .otherwise(lit("General Feedback"))
    )
    .withColumn(
        "NegativeFeedbackFlag",
        when(col("SentimentLabel") == "Negative", lit(1)).otherwise(lit(0))
    )
    .dropDuplicates(["ReviewID"])
)

# COMMAND ----------

# ============================================================
# Support Tickets Silver with issue classification
# ============================================================

silver_support_tickets = (
    df_support_tickets
    .select(
        trim(col("TicketID")).alias("TicketID"),
        trim(col("CustomerID")).alias("CustomerID"),
        trim(col("OrderID")).alias("OrderID"),
        to_timestamp(col("TicketDate")).alias("TicketDate"),
        trim(col("IssueCategory")).alias("IssueCategory"),
        trim(col("TicketText")).alias("TicketText"),
        trim(col("Priority")).alias("Priority"),
        trim(col("Status")).alias("Status"),
        col("ResolutionTimeHours").cast("double").alias("ResolutionTimeHours"),
        col("ingestion_timestamp"),
        col("source_file_path")
    )
    .filter(col("TicketID").isNotNull())
    .filter(col("TicketID") != "")
    .filter(col("CustomerID").isNotNull())
    .filter(col("OrderID").isNotNull())
    .filter(col("IssueCategory").isNotNull())
    .filter(col("IssueCategory") != "")
    .filter(col("Priority").isin("Low", "Medium", "High", "Critical"))
    .filter(col("Status").isin("Open", "In Progress", "Resolved", "Closed"))
    .filter((col("ResolutionTimeHours").isNull()) | (col("ResolutionTimeHours") >= 0))
    .withColumn(
        "IssueSeverityScore",
        when(col("Priority") == "Critical", lit(4))
        .when(col("Priority") == "High", lit(3))
        .when(col("Priority") == "Medium", lit(2))
        .otherwise(lit(1))
    )
    .withColumn(
        "SupplyChainImpactFlag",
        when(col("IssueCategory").isin("Delivery Issue", "Product Quality Issue", "Wrong Item", "Refund Issue"), lit(1))
        .otherwise(lit(0))
    )
    .withColumn(
        "PaymentLoginIssueFlag",
        when(col("IssueCategory").isin("Payment Issue", "Login Issue"), lit(1))
        .otherwise(lit(0))
    )
    .dropDuplicates(["TicketID"])
)

# COMMAND ----------

# ============================================================
# Chat Feedback Silver
# ============================================================

silver_chat_feedback = (
    df_chat_feedback
    .select(
        trim(col("chat_id")).alias("ChatID"),
        trim(col("customer.customer_id")).alias("CustomerID"),
        trim(col("customer.customer_name")).alias("CustomerName"),
        trim(col("customer.country")).alias("CustomerCountry"),
        trim(col("order_id")).alias("OrderID"),
        to_timestamp(col("chat_date")).alias("ChatDate"),
        trim(col("topic")).alias("Topic"),
        col("satisfaction_score").cast("int").alias("SatisfactionScore"),
        size(col("messages")).alias("MessageCount"),
        col("ingestion_timestamp"),
        col("source_file_path")
    )
    .filter(col("ChatID").isNotNull())
    .filter(col("ChatID") != "")
    .filter(col("CustomerID").isNotNull())
    .filter(col("OrderID").isNotNull())
    .filter((col("SatisfactionScore") >= 1) & (col("SatisfactionScore") <= 5))
    .withColumn(
        "ChatSentimentLabel",
        when(col("SatisfactionScore") >= 4, lit("Positive"))
        .when(col("SatisfactionScore") == 3, lit("Neutral"))
        .otherwise(lit("Negative"))
    )
    .withColumn(
        "ChatIssueCategory",
        when(lower(col("Topic")).contains("login"), lit("Login Issue"))
        .when(lower(col("Topic")).contains("payment"), lit("Payment Issue"))
        .when(lower(col("Topic")).contains("delivery"), lit("Delivery Issue"))
        .when(lower(col("Topic")).contains("damaged"), lit("Product Quality Issue"))
        .when(lower(col("Topic")).contains("refund"), lit("Refund Issue"))
        .when(lower(col("Topic")).contains("wrong item"), lit("Wrong Item"))
        .when(lower(col("Topic")).contains("stock"), lit("Stock Availability Issue"))
        .otherwise(lit("General Feedback"))
    )
    .dropDuplicates(["ChatID"])
)

silver_chat_messages = (
    df_chat_feedback
    .select(
        trim(col("chat_id")).alias("ChatID"),
        explode_outer(col("messages")).alias("Message")
    )
    .select(
        col("ChatID"),
        trim(col("Message.sender")).alias("Sender"),
        to_timestamp(col("Message.message_time")).alias("MessageTime"),
        trim(col("Message.message_text")).alias("MessageText")
    )
    .filter(col("ChatID").isNotNull())
    .filter(col("ChatID") != "")
)

# COMMAND ----------

# Write Silver tables
row_counts = {}

row_counts["silver_customers"] = write_silver_table(silver_customers, silver_customers_table)
row_counts["silver_products"] = write_silver_table(silver_products, silver_products_table)
row_counts["silver_orders"] = write_silver_table(silver_orders, silver_orders_table)
row_counts["silver_order_items"] = write_silver_table(silver_order_items, silver_order_items_table)
row_counts["silver_payments"] = write_silver_table(silver_payments, silver_payments_table)
row_counts["silver_shipments"] = write_silver_table(silver_shipments, silver_shipments_table)
row_counts["silver_returns"] = write_silver_table(silver_returns, silver_returns_table)
row_counts["silver_customer_reviews"] = write_silver_table(silver_customer_reviews, silver_customer_reviews_table)
row_counts["silver_support_tickets"] = write_silver_table(silver_support_tickets, silver_support_tickets_table)
row_counts["silver_chat_feedback"] = write_silver_table(silver_chat_feedback, silver_chat_feedback_table)
row_counts["silver_chat_messages"] = write_silver_table(silver_chat_messages, silver_chat_messages_table)

print("All Silver tables created successfully.")

# COMMAND ----------

# Display Silver row count validation summary
print("Silver row count validation summary:")

for table_name, count_value in row_counts.items():
    print(f"{table_name}: {count_value}")

# COMMAND ----------

# Quick table check
spark.sql(f"SHOW TABLES IN {silver_database}").show(truncate=False)

# COMMAND ----------

# Business validation samples

print("Review sentiment distribution:")
spark.sql(f"""
SELECT SentimentLabel, COUNT(*) AS ReviewCount
FROM {silver_customer_reviews_table}
GROUP BY SentimentLabel
ORDER BY ReviewCount DESC
""").show(truncate=False)

print("Support ticket issue distribution:")
spark.sql(f"""
SELECT IssueCategory, COUNT(*) AS TicketCount
FROM {silver_support_tickets_table}
GROUP BY IssueCategory
ORDER BY TicketCount DESC
""").show(truncate=False)

print("Chat issue distribution:")
spark.sql(f"""
SELECT ChatIssueCategory, COUNT(*) AS ChatCount
FROM {silver_chat_feedback_table}
GROUP BY ChatIssueCategory
ORDER BY ChatCount DESC
""").show(truncate=False)

# COMMAND ----------

print("Project 5 Silver customer intelligence completed successfully.")
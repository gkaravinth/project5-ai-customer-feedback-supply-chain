#run in separate cell (1st cell)
%run ./00_config

#run in separate cell (2nd cell)
# Databricks notebook source
# Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform
# Notebook: 03_gold_business_insights
# Purpose: Build Gold business-ready customer feedback and supply chain intelligence tables

# COMMAND ----------

from pyspark.sql.functions import (
    col,
    count,
    countDistinct,
    sum as spark_sum,
    avg,
    max as spark_max,
    min as spark_min,
    round as spark_round,
    when,
    lit,
    to_date,
    date_format
)

# COMMAND ----------

# Create Gold schema/database if it does not exist
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {gold_database}")

print(f"Gold database ready: {gold_database}")

# COMMAND ----------

def write_gold_table(df, table_name):
    """
    Write DataFrame as Delta table in Gold database.
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

# Load Silver tables
customers = spark.table(silver_customers_table)
products = spark.table(silver_products_table)
orders = spark.table(silver_orders_table)
order_items = spark.table(silver_order_items_table)
payments = spark.table(silver_payments_table)
shipments = spark.table(silver_shipments_table)
returns = spark.table(silver_returns_table)
reviews = spark.table(silver_customer_reviews_table)
tickets = spark.table(silver_support_tickets_table)
chat_feedback = spark.table(silver_chat_feedback_table)

print("All Silver tables loaded successfully.")

# COMMAND ----------

# ============================================================
# Gold 1: Product Feedback Summary
# ============================================================

gold_product_feedback_summary = (
    products.alias("p")
    .join(reviews.alias("r"), col("p.ProductID") == col("r.ProductID"), "left")
    .groupBy(
        col("p.ProductID"),
        col("p.SKU"),
        col("p.ProductName"),
        col("p.Category"),
        col("p.SubCategory"),
        col("p.Brand"),
        col("p.SupplierID")
    )
    .agg(
        count("r.ReviewID").alias("TotalReviews"),
        spark_round(avg("r.Rating"), 2).alias("AverageRating"),
        spark_sum(when(col("r.SentimentLabel") == "Positive", 1).otherwise(0)).alias("PositiveReviews"),
        spark_sum(when(col("r.SentimentLabel") == "Neutral", 1).otherwise(0)).alias("NeutralReviews"),
        spark_sum(when(col("r.SentimentLabel") == "Negative", 1).otherwise(0)).alias("NegativeReviews"),
        spark_sum(when(col("r.RecommendationFlag") == True, 1).otherwise(0)).alias("RecommendedReviewCount"),
        spark_sum(when(col("r.NegativeFeedbackFlag") == 1, 1).otherwise(0)).alias("NegativeFeedbackCount")
    )
    .withColumn(
        "PositiveReviewPct",
        spark_round((col("PositiveReviews") / when(col("TotalReviews") == 0, None).otherwise(col("TotalReviews"))) * 100, 2)
    )
    .withColumn(
        "NegativeReviewPct",
        spark_round((col("NegativeReviews") / when(col("TotalReviews") == 0, None).otherwise(col("TotalReviews"))) * 100, 2)
    )
    .withColumn(
        "RecommendationPct",
        spark_round((col("RecommendedReviewCount") / when(col("TotalReviews") == 0, None).otherwise(col("TotalReviews"))) * 100, 2)
    )
    .fillna({
        "TotalReviews": 0,
        "PositiveReviews": 0,
        "NeutralReviews": 0,
        "NegativeReviews": 0,
        "RecommendedReviewCount": 0,
        "NegativeFeedbackCount": 0
    })
)

# COMMAND ----------

# ============================================================
# Gold 2: Customer Complaint Summary
# ============================================================

ticket_summary = (
    tickets
    .groupBy("CustomerID")
    .agg(
        count("TicketID").alias("TotalTickets"),
        spark_sum(when(col("Priority") == "Critical", 1).otherwise(0)).alias("CriticalTickets"),
        spark_sum(when(col("Priority") == "High", 1).otherwise(0)).alias("HighTickets"),
        spark_sum("SupplyChainImpactFlag").alias("SupplyChainImpactTickets"),
        spark_sum("PaymentLoginIssueFlag").alias("PaymentLoginIssueTickets"),
        spark_round(avg("IssueSeverityScore"), 2).alias("AvgIssueSeverityScore")
    )
)

review_summary = (
    reviews
    .groupBy("CustomerID")
    .agg(
        count("ReviewID").alias("TotalReviews"),
        spark_sum("NegativeFeedbackFlag").alias("NegativeReviews"),
        spark_round(avg("Rating"), 2).alias("AvgCustomerRating")
    )
)

chat_summary = (
    chat_feedback
    .groupBy("CustomerID")
    .agg(
        count("ChatID").alias("TotalChats"),
        spark_sum(when(col("ChatSentimentLabel") == "Negative", 1).otherwise(0)).alias("NegativeChats"),
        spark_round(avg("SatisfactionScore"), 2).alias("AvgChatSatisfaction")
    )
)

gold_customer_complaint_summary = (
    customers
    .join(ticket_summary, "CustomerID", "left")
    .join(review_summary, "CustomerID", "left")
    .join(chat_summary, "CustomerID", "left")
    .fillna({
        "TotalTickets": 0,
        "CriticalTickets": 0,
        "HighTickets": 0,
        "SupplyChainImpactTickets": 0,
        "PaymentLoginIssueTickets": 0,
        "TotalReviews": 0,
        "NegativeReviews": 0,
        "TotalChats": 0,
        "NegativeChats": 0
    })
    .withColumn(
        "CustomerRiskLevel",
        when((col("CriticalTickets") > 0) | (col("NegativeReviews") >= 2), lit("High Risk"))
        .when((col("HighTickets") > 0) | (col("NegativeChats") >= 2), lit("Medium Risk"))
        .otherwise(lit("Low Risk"))
    )
)

# COMMAND ----------

# ============================================================
# Gold 3: Delivery Issue Analysis
# ============================================================

gold_delivery_issue_analysis = (
    shipments.alias("s")
    .join(orders.alias("o"), col("s.OrderID") == col("o.OrderID"), "left")
    .join(customers.alias("c"), col("o.CustomerID") == col("c.CustomerID"), "left")
    .groupBy(
        col("s.DeliveryCountry"),
        col("s.Carrier"),
        col("s.DeliveryStatus")
    )
    .agg(
        count("s.ShipmentID").alias("TotalShipments"),
        spark_sum("s.DeliveryIssueFlag").alias("DeliveryIssueCount"),
        spark_round(avg("s.DeliveryDelayDays"), 2).alias("AvgDeliveryDelayDays"),
        countDistinct("o.CustomerID").alias("AffectedCustomers")
    )
    .withColumn(
        "DeliveryIssuePct",
        spark_round((col("DeliveryIssueCount") / col("TotalShipments")) * 100, 2)
    )
    .withColumn(
        "DeliveryRiskLevel",
        when(col("DeliveryIssuePct") >= 30, lit("High"))
        .when(col("DeliveryIssuePct") >= 15, lit("Medium"))
        .otherwise(lit("Low"))
    )
)

# COMMAND ----------

# ============================================================
# Gold 4: Payment and Login Issue Analysis
# ============================================================

payment_issue_summary = (
    payments
    .groupBy("PaymentStatus", "PaymentMethod", "PaymentFailureReason")
    .agg(
        count("PaymentID").alias("PaymentRecordCount"),
        spark_sum("PaymentIssueFlag").alias("PaymentIssueCount"),
        spark_round(spark_sum("Amount"), 2).alias("TotalPaymentAmount")
    )
)

login_ticket_summary = (
    tickets
    .filter(col("IssueCategory") == "Login Issue")
    .groupBy("IssueCategory", "Priority", "Status")
    .agg(
        count("TicketID").alias("LoginTicketCount"),
        spark_round(avg("ResolutionTimeHours"), 2).alias("AvgResolutionHours")
    )
)

gold_payment_login_issue_analysis = (
    payment_issue_summary
    .withColumn("AnalysisType", lit("Payment"))
    .select(
        "AnalysisType",
        col("PaymentStatus").alias("IssueStatus"),
        col("PaymentMethod").alias("IssueMethodOrPriority"),
        col("PaymentFailureReason").alias("IssueReasonOrTicketStatus"),
        col("PaymentRecordCount").alias("RecordCount"),
        col("PaymentIssueCount").alias("IssueCount"),
        col("TotalPaymentAmount").alias("AmountOrAvgResolution")
    )
    .unionByName(
        login_ticket_summary
        .withColumn("AnalysisType", lit("Login"))
        .select(
            "AnalysisType",
            col("IssueCategory").alias("IssueStatus"),
            col("Priority").alias("IssueMethodOrPriority"),
            col("Status").alias("IssueReasonOrTicketStatus"),
            col("LoginTicketCount").alias("RecordCount"),
            col("LoginTicketCount").alias("IssueCount"),
            col("AvgResolutionHours").alias("AmountOrAvgResolution")
        )
    )
)

# COMMAND ----------

# ============================================================
# Gold 5: Return Reason Analysis
# ============================================================

gold_return_reason_analysis = (
    returns.alias("r")
    .join(products.alias("p"), col("r.ProductID") == col("p.ProductID"), "left")
    .groupBy(
        col("r.ReturnReason"),
        col("p.Category"),
        col("p.Brand")
    )
    .agg(
        count("r.ReturnID").alias("ReturnCount"),
        spark_sum("r.ReturnQty").alias("TotalReturnedQty"),
        spark_round(spark_sum("r.RefundAmount"), 2).alias("TotalRefundAmount"),
        spark_sum("r.SupplyChainReturnFlag").alias("SupplyChainRelatedReturns")
    )
    .withColumn(
        "ReturnRiskLevel",
        when(col("SupplyChainRelatedReturns") >= 10, lit("High"))
        .when(col("SupplyChainRelatedReturns") >= 5, lit("Medium"))
        .otherwise(lit("Low"))
    )
)

# COMMAND ----------

# ============================================================
# Gold 6: Product Recommendation Ranking
# ============================================================

sales_by_product = (
    order_items
    .groupBy("ProductID")
    .agg(
        spark_sum("Quantity").alias("TotalUnitsSold"),
        spark_round(spark_sum("LineTotal"), 2).alias("TotalSalesValue")
    )
)

gold_product_recommendation_ranking = (
    gold_product_feedback_summary.alias("f")
    .join(sales_by_product.alias("s"), col("f.ProductID") == col("s.ProductID"), "left")
    .select(
        col("f.ProductID"),
        col("f.SKU"),
        col("f.ProductName"),
        col("f.Category"),
        col("f.Brand"),
        col("f.TotalReviews"),
        col("f.AverageRating"),
        col("f.PositiveReviewPct"),
        col("f.NegativeReviewPct"),
        col("f.RecommendationPct"),
        col("s.TotalUnitsSold"),
        col("s.TotalSalesValue")
    )
    .fillna({
        "TotalUnitsSold": 0,
        "TotalSalesValue": 0
    })
    .withColumn(
        "RecommendationRankScore",
        spark_round(
            (
                (when(col("AverageRating").isNull(), lit(0)).otherwise(col("AverageRating")) * 20) +
                (when(col("RecommendationPct").isNull(), lit(0)).otherwise(col("RecommendationPct")) * 0.5) +
                (when(col("PositiveReviewPct").isNull(), lit(0)).otherwise(col("PositiveReviewPct")) * 0.3) -
                (when(col("NegativeReviewPct").isNull(), lit(0)).otherwise(col("NegativeReviewPct")) * 0.4)
            ),
            2
        )
    )
    .withColumn(
        "RecommendationLevel",
        when(col("RecommendationRankScore") >= 100, lit("Highly Recommended"))
        .when(col("RecommendationRankScore") >= 70, lit("Recommended"))
        .when(col("RecommendationRankScore") >= 40, lit("Average"))
        .otherwise(lit("Low Recommendation"))
    )
)

# COMMAND ----------

# ============================================================
# Gold 7: Customer Sentiment Trend
# ============================================================

gold_customer_sentiment_trend = (
    reviews
    .withColumn("ReviewMonth", date_format(col("ReviewDate"), "yyyy-MM"))
    .groupBy("ReviewMonth", "SentimentLabel", "ReviewIssueCategory")
    .agg(
        count("ReviewID").alias("ReviewCount"),
        spark_round(avg("Rating"), 2).alias("AvgRating")
    )
    .orderBy("ReviewMonth", "SentimentLabel")
)

# COMMAND ----------

# ============================================================
# Gold 8: Supply Chain Customer Risk
# ============================================================

return_product_issues = (
    returns
    .groupBy("ProductID")
    .agg(
        count("ReturnID").alias("ReturnCount"),
        spark_sum("SupplyChainReturnFlag").alias("SupplyChainReturnCount")
    )
)

review_product_issues = (
    reviews
    .groupBy("ProductID")
    .agg(
        count("ReviewID").alias("ReviewCount"),
        spark_sum("NegativeFeedbackFlag").alias("NegativeReviewCount")
    )
)

gold_supply_chain_customer_risk = (
    products.alias("p")
    .join(return_product_issues.alias("r"), col("p.ProductID") == col("r.ProductID"), "left")
    .join(review_product_issues.alias("rv"), col("p.ProductID") == col("rv.ProductID"), "left")
    .select(
        col("p.ProductID"),
        col("p.ProductName"),
        col("p.Category"),
        col("p.Brand"),
        col("p.SupplierID"),
        col("r.ReturnCount"),
        col("r.SupplyChainReturnCount"),
        col("rv.ReviewCount"),
        col("rv.NegativeReviewCount")
    )
    .fillna({
        "ReturnCount": 0,
        "SupplyChainReturnCount": 0,
        "ReviewCount": 0,
        "NegativeReviewCount": 0
    })
    .withColumn(
        "SupplyChainRiskScore",
        (col("SupplyChainReturnCount") * 3) + (col("NegativeReviewCount") * 2)
    )
    .withColumn(
        "SupplyChainRiskLevel",
        when(col("SupplyChainRiskScore") >= 20, lit("High"))
        .when(col("SupplyChainRiskScore") >= 10, lit("Medium"))
        .otherwise(lit("Low"))
    )
)

# COMMAND ----------

# Write Gold tables
row_counts = {}

row_counts["gold_product_feedback_summary"] = write_gold_table(
    gold_product_feedback_summary,
    gold_product_feedback_summary_table
)

row_counts["gold_customer_complaint_summary"] = write_gold_table(
    gold_customer_complaint_summary,
    gold_customer_complaint_summary_table
)

row_counts["gold_delivery_issue_analysis"] = write_gold_table(
    gold_delivery_issue_analysis,
    gold_delivery_issue_analysis_table
)

row_counts["gold_payment_login_issue_analysis"] = write_gold_table(
    gold_payment_login_issue_analysis,
    gold_payment_login_issue_analysis_table
)

row_counts["gold_return_reason_analysis"] = write_gold_table(
    gold_return_reason_analysis,
    gold_return_reason_analysis_table
)

row_counts["gold_product_recommendation_ranking"] = write_gold_table(
    gold_product_recommendation_ranking,
    gold_product_recommendation_ranking_table
)

row_counts["gold_customer_sentiment_trend"] = write_gold_table(
    gold_customer_sentiment_trend,
    gold_customer_sentiment_trend_table
)

row_counts["gold_supply_chain_customer_risk"] = write_gold_table(
    gold_supply_chain_customer_risk,
    gold_supply_chain_customer_risk_table
)

print("All Gold tables created successfully.")

# COMMAND ----------

# Display Gold row count validation summary
print("Gold row count validation summary:")

for table_name, count_value in row_counts.items():
    print(f"{table_name}: {count_value}")

# COMMAND ----------

# Quick table check
spark.sql(f"SHOW TABLES IN {gold_database}").show(truncate=False)

# COMMAND ----------

# Business validation samples

print("Top product recommendation ranking:")
spark.sql(f"""
SELECT
    ProductID,
    ProductName,
    Category,
    AverageRating,
    RecommendationPct,
    RecommendationRankScore,
    RecommendationLevel
FROM {gold_product_recommendation_ranking_table}
ORDER BY RecommendationRankScore DESC
LIMIT 10
""").show(truncate=False)

print("High supply chain customer risk products:")
spark.sql(f"""
SELECT
    ProductID,
    ProductName,
    Category,
    SupplierID,
    SupplyChainRiskScore,
    SupplyChainRiskLevel
FROM {gold_supply_chain_customer_risk_table}
ORDER BY SupplyChainRiskScore DESC
LIMIT 10
""").show(truncate=False)

print("Delivery issue analysis:")
spark.sql(f"""
SELECT
    DeliveryCountry,
    Carrier,
    DeliveryStatus,
    TotalShipments,
    DeliveryIssueCount,
    DeliveryIssuePct,
    DeliveryRiskLevel
FROM {gold_delivery_issue_analysis_table}
ORDER BY DeliveryIssuePct DESC
LIMIT 10
""").show(truncate=False)

# COMMAND ----------

print("Project 5 Gold business insights completed successfully.")



```sql
-- Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform
-- File: 01_validation_queries.sql
-- Purpose: Validation queries for Bronze, Silver, and Gold tables

-- ============================================================
-- 1. Bronze table row count validation
-- ============================================================

SELECT 'bronze_customers' AS table_name, COUNT(*) AS row_count
FROM supplyspark.project5_bronze.bronze_customers
UNION ALL
SELECT 'bronze_products', COUNT(*)
FROM supplyspark.project5_bronze.bronze_products
UNION ALL
SELECT 'bronze_orders', COUNT(*)
FROM supplyspark.project5_bronze.bronze_orders
UNION ALL
SELECT 'bronze_order_items', COUNT(*)
FROM supplyspark.project5_bronze.bronze_order_items
UNION ALL
SELECT 'bronze_payments', COUNT(*)
FROM supplyspark.project5_bronze.bronze_payments
UNION ALL
SELECT 'bronze_shipments', COUNT(*)
FROM supplyspark.project5_bronze.bronze_shipments
UNION ALL
SELECT 'bronze_returns', COUNT(*)
FROM supplyspark.project5_bronze.bronze_returns
UNION ALL
SELECT 'bronze_customer_reviews', COUNT(*)
FROM supplyspark.project5_bronze.bronze_customer_reviews
UNION ALL
SELECT 'bronze_support_tickets', COUNT(*)
FROM supplyspark.project5_bronze.bronze_support_tickets
UNION ALL
SELECT 'bronze_chat_feedback_raw', COUNT(*)
FROM supplyspark.project5_bronze.bronze_chat_feedback_raw;


-- ============================================================
-- 2. Silver table row count validation
-- ============================================================

SELECT 'silver_customers' AS table_name, COUNT(*) AS row_count
FROM supplyspark.project5_silver.silver_customers
UNION ALL
SELECT 'silver_products', COUNT(*)
FROM supplyspark.project5_silver.silver_products
UNION ALL
SELECT 'silver_orders', COUNT(*)
FROM supplyspark.project5_silver.silver_orders
UNION ALL
SELECT 'silver_order_items', COUNT(*)
FROM supplyspark.project5_silver.silver_order_items
UNION ALL
SELECT 'silver_payments', COUNT(*)
FROM supplyspark.project5_silver.silver_payments
UNION ALL
SELECT 'silver_shipments', COUNT(*)
FROM supplyspark.project5_silver.silver_shipments
UNION ALL
SELECT 'silver_returns', COUNT(*)
FROM supplyspark.project5_silver.silver_returns
UNION ALL
SELECT 'silver_customer_reviews', COUNT(*)
FROM supplyspark.project5_silver.silver_customer_reviews
UNION ALL
SELECT 'silver_support_tickets', COUNT(*)
FROM supplyspark.project5_silver.silver_support_tickets
UNION ALL
SELECT 'silver_chat_feedback', COUNT(*)
FROM supplyspark.project5_silver.silver_chat_feedback
UNION ALL
SELECT 'silver_chat_messages', COUNT(*)
FROM supplyspark.project5_silver.silver_chat_messages;


-- ============================================================
-- 3. Gold table row count validation
-- ============================================================

SELECT 'gold_product_feedback_summary' AS table_name, COUNT(*) AS row_count
FROM supplyspark.project5_gold.gold_product_feedback_summary
UNION ALL
SELECT 'gold_customer_complaint_summary', COUNT(*)
FROM supplyspark.project5_gold.gold_customer_complaint_summary
UNION ALL
SELECT 'gold_delivery_issue_analysis', COUNT(*)
FROM supplyspark.project5_gold.gold_delivery_issue_analysis
UNION ALL
SELECT 'gold_payment_login_issue_analysis', COUNT(*)
FROM supplyspark.project5_gold.gold_payment_login_issue_analysis
UNION ALL
SELECT 'gold_return_reason_analysis', COUNT(*)
FROM supplyspark.project5_gold.gold_return_reason_analysis
UNION ALL
SELECT 'gold_product_recommendation_ranking', COUNT(*)
FROM supplyspark.project5_gold.gold_product_recommendation_ranking
UNION ALL
SELECT 'gold_customer_sentiment_trend', COUNT(*)
FROM supplyspark.project5_gold.gold_customer_sentiment_trend
UNION ALL
SELECT 'gold_supply_chain_customer_risk', COUNT(*)
FROM supplyspark.project5_gold.gold_supply_chain_customer_risk;


-- ============================================================
-- 4. Data quality validation - invalid values should be zero
-- ============================================================

SELECT COUNT(*) AS invalid_product_count
FROM supplyspark.project5_silver.silver_products
WHERE ProductID IS NULL
   OR ProductID = ''
   OR UnitCost < 0
   OR RetailPrice < 0
   OR Currency <> 'EUR';


SELECT COUNT(*) AS invalid_order_count
FROM supplyspark.project5_silver.silver_orders
WHERE OrderID IS NULL
   OR OrderID = ''
   OR GrossAmount < 0
   OR DiscountAmount < 0
   OR NetAmount < 0
   OR Currency <> 'EUR';


SELECT COUNT(*) AS invalid_review_count
FROM supplyspark.project5_silver.silver_customer_reviews
WHERE ReviewID IS NULL
   OR ReviewID = ''
   OR Rating NOT BETWEEN 1 AND 5
   OR ReviewText IS NULL
   OR ReviewText = '';


SELECT COUNT(*) AS invalid_ticket_count
FROM supplyspark.project5_silver.silver_support_tickets
WHERE TicketID IS NULL
   OR TicketID = ''
   OR Priority NOT IN ('Low', 'Medium', 'High', 'Critical')
   OR Status NOT IN ('Open', 'In Progress', 'Resolved', 'Closed');


-- ============================================================
-- 5. Business rule validation
-- ============================================================

SELECT SentimentLabel, COUNT(*) AS review_count
FROM supplyspark.project5_silver.silver_customer_reviews
GROUP BY SentimentLabel
ORDER BY review_count DESC;


SELECT IssueCategory, COUNT(*) AS ticket_count
FROM supplyspark.project5_silver.silver_support_tickets
GROUP BY IssueCategory
ORDER BY ticket_count DESC;


SELECT ChatIssueCategory, COUNT(*) AS chat_count
FROM supplyspark.project5_silver.silver_chat_feedback
GROUP BY ChatIssueCategory
ORDER BY chat_count DESC;


SELECT CustomerRiskLevel, COUNT(*) AS customer_count
FROM supplyspark.project5_gold.gold_customer_complaint_summary
GROUP BY CustomerRiskLevel
ORDER BY customer_count DESC;


SELECT SupplyChainRiskLevel, COUNT(*) AS product_count
FROM supplyspark.project5_gold.gold_supply_chain_customer_risk
GROUP BY SupplyChainRiskLevel
ORDER BY product_count DESC;
```

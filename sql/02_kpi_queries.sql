-- Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform
-- File: 02_kpi_queries.sql
-- Purpose: KPI queries for customer feedback and supply chain intelligence

-- ============================================================
-- 1. Top recommended products
-- ============================================================

SELECT
    ProductID,
    ProductName,
    Category,
    Brand,
    AverageRating,
    RecommendationPct,
    PositiveReviewPct,
    NegativeReviewPct,
    TotalUnitsSold,
    TotalSalesValue,
    RecommendationRankScore,
    RecommendationLevel
FROM supplyspark.project5_gold.gold_product_recommendation_ranking
ORDER BY RecommendationRankScore DESC
LIMIT 10;


-- ============================================================
-- 2. Products with highest supply chain customer risk
-- ============================================================

SELECT
    ProductID,
    ProductName,
    Category,
    Brand,
    SupplierID,
    ReturnCount,
    SupplyChainReturnCount,
    ReviewCount,
    NegativeReviewCount,
    SupplyChainRiskScore,
    SupplyChainRiskLevel
FROM supplyspark.project5_gold.gold_supply_chain_customer_risk
ORDER BY SupplyChainRiskScore DESC
LIMIT 10;


-- ============================================================
-- 3. Customer complaint risk summary
-- ============================================================

SELECT
    CustomerRiskLevel,
    COUNT(*) AS CustomerCount,
    SUM(TotalTickets) AS TotalTickets,
    SUM(NegativeReviews) AS NegativeReviews,
    SUM(NegativeChats) AS NegativeChats
FROM supplyspark.project5_gold.gold_customer_complaint_summary
GROUP BY CustomerRiskLevel
ORDER BY CustomerCount DESC;


-- ============================================================
-- 4. Delivery issue performance
-- ============================================================

SELECT
    DeliveryCountry,
    Carrier,
    DeliveryStatus,
    TotalShipments,
    DeliveryIssueCount,
    AvgDeliveryDelayDays,
    AffectedCustomers,
    DeliveryIssuePct,
    DeliveryRiskLevel
FROM supplyspark.project5_gold.gold_delivery_issue_analysis
ORDER BY DeliveryIssuePct DESC
LIMIT 20;


-- ============================================================
-- 5. Payment and login issue analysis
-- ============================================================

SELECT
    AnalysisType,
    IssueStatus,
    IssueMethodOrPriority,
    IssueReasonOrTicketStatus,
    RecordCount,
    IssueCount,
    AmountOrAvgResolution
FROM supplyspark.project5_gold.gold_payment_login_issue_analysis
ORDER BY IssueCount DESC;


-- ============================================================
-- 6. Return reason analysis
-- ============================================================

SELECT
    ReturnReason,
    Category,
    Brand,
    ReturnCount,
    TotalReturnedQty,
    TotalRefundAmount,
    SupplyChainRelatedReturns,
    ReturnRiskLevel
FROM supplyspark.project5_gold.gold_return_reason_analysis
ORDER BY SupplyChainRelatedReturns DESC, ReturnCount DESC
LIMIT 20;


-- ============================================================
-- 7. Customer sentiment trend
-- ============================================================

SELECT
    ReviewMonth,
    SentimentLabel,
    ReviewIssueCategory,
    ReviewCount,
    AvgRating
FROM supplyspark.project5_gold.gold_customer_sentiment_trend
ORDER BY ReviewMonth, SentimentLabel, ReviewIssueCategory;


-- ============================================================
-- 8. Product feedback summary
-- ============================================================

SELECT
    ProductID,
    SKU,
    ProductName,
    Category,
    SubCategory,
    Brand,
    SupplierID,
    TotalReviews,
    AverageRating,
    PositiveReviews,
    NeutralReviews,
    NegativeReviews,
    RecommendedReviewCount,
    PositiveReviewPct,
    NegativeReviewPct,
    RecommendationPct
FROM supplyspark.project5_gold.gold_product_feedback_summary
ORDER BY TotalReviews DESC, AverageRating DESC
LIMIT 20;


-- ============================================================
-- 9. Negative feedback products
-- ============================================================

SELECT
    ProductID,
    ProductName,
    Category,
    Brand,
    TotalReviews,
    AverageRating,
    NegativeReviews,
    NegativeReviewPct
FROM supplyspark.project5_gold.gold_product_feedback_summary
WHERE NegativeReviews > 0
ORDER BY NegativeReviewPct DESC, NegativeReviews DESC
LIMIT 20;


-- ============================================================
-- 10. Executive KPI summary
-- ============================================================

SELECT
    (SELECT COUNT(*) FROM supplyspark.project5_silver.silver_orders) AS TotalOrders,
    (SELECT COUNT(*) FROM supplyspark.project5_silver.silver_customers) AS TotalCustomers,
    (SELECT COUNT(*) FROM supplyspark.project5_silver.silver_customer_reviews) AS TotalReviews,
    (SELECT COUNT(*) FROM supplyspark.project5_silver.silver_support_tickets) AS TotalSupportTickets,
    (SELECT COUNT(*) FROM supplyspark.project5_silver.silver_returns) AS TotalReturns,
    (SELECT COUNT(*) FROM supplyspark.project5_silver.silver_chat_feedback) AS TotalChatFeedback,
    (SELECT COUNT(*) FROM supplyspark.project5_gold.gold_product_recommendation_ranking WHERE RecommendationLevel = 'Highly Recommended') AS HighlyRecommendedProducts,
    (SELECT COUNT(*) FROM supplyspark.project5_gold.gold_customer_complaint_summary WHERE CustomerRiskLevel = 'High Risk') AS HighRiskCustomers,
    (SELECT COUNT(*) FROM supplyspark.project5_gold.gold_supply_chain_customer_risk WHERE SupplyChainRiskLevel = 'High') AS HighSupplyChainRiskProducts;
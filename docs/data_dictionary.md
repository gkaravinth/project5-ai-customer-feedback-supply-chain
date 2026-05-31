# Data Dictionary

## Project

Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform

## Scope

This data dictionary describes the main source files, Bronze tables, Silver tables, and Gold tables used in Project 5.

The project focuses on customer feedback analytics and supply chain intelligence using rule-based PySpark classification.

A full RAG system is not implemented in this version. RAG is listed as a future enhancement.

---

# Source Files

## customers.csv

| Column          | Description                                             |
| --------------- | ------------------------------------------------------- |
| CustomerID      | Unique customer identifier                              |
| CustomerName    | Customer full name                                      |
| Email           | Customer email address                                  |
| Country         | Customer country                                        |
| City            | Customer city                                           |
| SignupDate      | Customer account signup date                            |
| CustomerSegment | Customer segment such as Standard, Silver, Gold, or VIP |
| IsActive        | Indicates whether the customer account is active        |

## products.csv

| Column      | Description                             |
| ----------- | --------------------------------------- |
| ProductID   | Unique product identifier               |
| SKU         | Product SKU code                        |
| ProductName | Product name                            |
| Category    | Product category                        |
| SubCategory | Product subcategory                     |
| Brand       | Product brand                           |
| SupplierID  | Supplier identifier                     |
| UnitCost    | Product unit cost                       |
| RetailPrice | Product selling price                   |
| Currency    | Transaction currency                    |
| IsActive    | Indicates whether the product is active |

## orders.csv

| Column         | Description                             |
| -------------- | --------------------------------------- |
| OrderID        | Unique order identifier                 |
| CustomerID     | Customer linked to the order            |
| OrderDate      | Date and time when the order was placed |
| OrderStatus    | Order status                            |
| SalesChannel   | Website or mobile app                   |
| GrossAmount    | Order value before discount             |
| DiscountAmount | Discount applied to the order           |
| NetAmount      | Final order amount after discount       |
| Currency       | Transaction currency                    |

## order_items.csv

| Column      | Description                       |
| ----------- | --------------------------------- |
| OrderItemID | Unique order line identifier      |
| OrderID     | Related order                     |
| ProductID   | Related product                   |
| Quantity    | Ordered quantity                  |
| UnitPrice   | Selling price per unit            |
| LineTotal   | Quantity multiplied by unit price |

## payments.csv

| Column               | Description                            |
| -------------------- | -------------------------------------- |
| PaymentID            | Unique payment identifier              |
| OrderID              | Related order                          |
| PaymentDate          | Payment date and time                  |
| PaymentMethod        | Card, PayPal, wallet, or bank transfer |
| PaymentStatus        | Paid, Failed, Pending, or Refunded     |
| PaymentFailureReason | Reason for failed payment              |
| Amount               | Payment amount                         |
| Currency             | Transaction currency                   |

## shipments.csv

| Column               | Description                             |
| -------------------- | --------------------------------------- |
| ShipmentID           | Unique shipment identifier              |
| OrderID              | Related order                           |
| WarehouseID          | Warehouse responsible for shipment      |
| Carrier              | Delivery carrier                        |
| ShipmentDate         | Date shipment was created               |
| ExpectedDeliveryDate | Expected delivery date                  |
| ActualDeliveryDate   | Actual delivery date                    |
| DeliveryStatus       | Delivered, In Transit, Delayed, or Lost |
| DeliveryCountry      | Delivery destination country            |

## returns.csv

| Column       | Description              |
| ------------ | ------------------------ |
| ReturnID     | Unique return identifier |
| OrderID      | Related order            |
| ProductID    | Returned product         |
| ReturnDate   | Return date              |
| ReturnQty    | Returned quantity        |
| ReturnReason | Reason for return        |
| RefundAmount | Refund amount            |

## customer_reviews.csv

| Column             | Description                                       |
| ------------------ | ------------------------------------------------- |
| ReviewID           | Unique review identifier                          |
| OrderID            | Related order                                     |
| CustomerID         | Customer who submitted the review                 |
| ProductID          | Product reviewed                                  |
| ReviewDate         | Review date                                       |
| Rating             | Customer rating from 1 to 5                       |
| ReviewText         | Written customer review                           |
| RecommendationFlag | Indicates whether customer recommends the product |

## support_tickets.csv

| Column              | Description                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------- |
| TicketID            | Unique support ticket identifier                                                            |
| CustomerID          | Customer who raised the ticket                                                              |
| OrderID             | Related order                                                                               |
| TicketDate          | Ticket created date and time                                                                |
| IssueCategory       | Issue category such as Login Issue, Payment Issue, Delivery Issue, or Product Quality Issue |
| TicketText          | Customer support ticket description                                                         |
| Priority            | Low, Medium, High, or Critical                                                              |
| Status              | Open, In Progress, Resolved, or Closed                                                      |
| ResolutionTimeHours | Time taken to resolve the ticket                                                            |

## chat_feedback.json

| Field                  | Description                             |
| ---------------------- | --------------------------------------- |
| chat_id                | Unique chat identifier                  |
| customer.customer_id   | Customer identifier                     |
| customer.customer_name | Customer name                           |
| customer.country       | Customer country                        |
| order_id               | Related order                           |
| chat_date              | Chat date and time                      |
| topic                  | Main chat topic                         |
| satisfaction_score     | Customer satisfaction score from 1 to 5 |
| messages               | Nested chat messages                    |

---

# Bronze Layer

Bronze tables store raw data from the Azure Storage raw zone as Delta tables.

Each Bronze table includes ingestion metadata:

| Column              | Description                            |
| ------------------- | -------------------------------------- |
| ingestion_timestamp | Timestamp when the record was ingested |
| source_file_path    | Source file path from Azure Storage    |

## Bronze Tables

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

---

# Silver Layer

Silver tables contain cleaned, filtered, standardized, and classified data.

## Silver Tables

* silver_customers
* silver_products
* silver_orders
* silver_order_items
* silver_payments
* silver_shipments
* silver_returns
* silver_customer_reviews
* silver_support_tickets
* silver_chat_feedback
* silver_chat_messages

## Important Silver Columns

| Column                | Table                   | Description                                                            |
| --------------------- | ----------------------- | ---------------------------------------------------------------------- |
| PaymentIssueFlag      | silver_payments         | 1 when payment status is Failed                                        |
| DeliveryDelayDays     | silver_shipments        | Difference between actual and expected delivery date                   |
| DeliveryIssueFlag     | silver_shipments        | 1 when delivery is delayed, lost, or delivered late                    |
| SupplyChainReturnFlag | silver_returns          | 1 when return reason suggests product, delivery, or supply chain issue |
| SentimentLabel        | silver_customer_reviews | Positive, Neutral, or Negative based on rating                         |
| ReviewIssueCategory   | silver_customer_reviews | Classified issue category based on review text                         |
| NegativeFeedbackFlag  | silver_customer_reviews | 1 when sentiment is Negative                                           |
| IssueSeverityScore    | silver_support_tickets  | Numeric score based on ticket priority                                 |
| SupplyChainImpactFlag | silver_support_tickets  | 1 for delivery, product quality, wrong item, or refund-related issues  |
| PaymentLoginIssueFlag | silver_support_tickets  | 1 for payment or login issues                                          |
| ChatSentimentLabel    | silver_chat_feedback    | Positive, Neutral, or Negative based on satisfaction score             |
| ChatIssueCategory     | silver_chat_feedback    | Classified issue category based on chat topic                          |
| MessageCount          | silver_chat_feedback    | Number of messages in the chat                                         |

---

# Gold Layer

Gold tables are business-ready analytical tables.

## gold_product_feedback_summary

Summarizes customer review performance by product.

| Column                 | Description                                   |
| ---------------------- | --------------------------------------------- |
| ProductID              | Product identifier                            |
| SKU                    | Product SKU                                   |
| ProductName            | Product name                                  |
| Category               | Product category                              |
| SubCategory            | Product subcategory                           |
| Brand                  | Product brand                                 |
| SupplierID             | Supplier identifier                           |
| TotalReviews           | Total number of reviews                       |
| AverageRating          | Average customer rating                       |
| PositiveReviews        | Count of positive reviews                     |
| NeutralReviews         | Count of neutral reviews                      |
| NegativeReviews        | Count of negative reviews                     |
| RecommendedReviewCount | Count of reviews where product is recommended |
| NegativeFeedbackCount  | Count of negative feedback records            |
| PositiveReviewPct      | Positive review percentage                    |
| NegativeReviewPct      | Negative review percentage                    |
| RecommendationPct      | Product recommendation percentage             |

## gold_customer_complaint_summary

Combines customer, ticket, review, and chat data to classify customer risk.

| Column                   | Description                                 |
| ------------------------ | ------------------------------------------- |
| CustomerID               | Customer identifier                         |
| CustomerName             | Customer name                               |
| Email                    | Customer email                              |
| Country                  | Customer country                            |
| City                     | Customer city                               |
| CustomerSegment          | Customer segment                            |
| TotalTickets             | Total support tickets                       |
| CriticalTickets          | Critical support ticket count               |
| HighTickets              | High-priority support ticket count          |
| SupplyChainImpactTickets | Tickets linked to supply chain impact       |
| PaymentLoginIssueTickets | Tickets linked to payment or login problems |
| AvgIssueSeverityScore    | Average issue severity                      |
| TotalReviews             | Total reviews submitted                     |
| NegativeReviews          | Negative reviews submitted                  |
| AvgCustomerRating        | Average rating from customer                |
| TotalChats               | Total chat interactions                     |
| NegativeChats            | Negative chat interactions                  |
| AvgChatSatisfaction      | Average chat satisfaction score             |
| CustomerRiskLevel        | Low Risk, Medium Risk, or High Risk         |

## gold_delivery_issue_analysis

Analyzes delivery performance by country, carrier, and delivery status.

| Column               | Description                 |
| -------------------- | --------------------------- |
| DeliveryCountry      | Delivery country            |
| Carrier              | Delivery carrier            |
| DeliveryStatus       | Delivery status             |
| TotalShipments       | Total shipment count        |
| DeliveryIssueCount   | Delivery issue count        |
| AvgDeliveryDelayDays | Average delivery delay days |
| AffectedCustomers    | Count of affected customers |
| DeliveryIssuePct     | Delivery issue percentage   |
| DeliveryRiskLevel    | Low, Medium, or High        |

## gold_payment_login_issue_analysis

Combines payment failure analysis and login issue ticket analysis.

| Column                    | Description                                |
| ------------------------- | ------------------------------------------ |
| AnalysisType              | Payment or Login                           |
| IssueStatus               | Payment status or login issue category     |
| IssueMethodOrPriority     | Payment method or ticket priority          |
| IssueReasonOrTicketStatus | Failure reason or ticket status            |
| RecordCount               | Number of records                          |
| IssueCount                | Number of issue records                    |
| AmountOrAvgResolution     | Payment amount or average resolution hours |

## gold_return_reason_analysis

Analyzes product returns by return reason, category, and brand.

| Column                    | Description                                  |
| ------------------------- | -------------------------------------------- |
| ReturnReason              | Reason for return                            |
| Category                  | Product category                             |
| Brand                     | Product brand                                |
| ReturnCount               | Number of returns                            |
| TotalReturnedQty          | Total returned quantity                      |
| TotalRefundAmount         | Total refund amount                          |
| SupplyChainRelatedReturns | Returns linked to supply chain/product issue |
| ReturnRiskLevel           | Low, Medium, or High                         |

## gold_product_recommendation_ranking

Ranks products based on ratings, recommendation percentage, feedback, and sales.

| Column                  | Description                                                     |
| ----------------------- | --------------------------------------------------------------- |
| ProductID               | Product identifier                                              |
| SKU                     | Product SKU                                                     |
| ProductName             | Product name                                                    |
| Category                | Product category                                                |
| Brand                   | Product brand                                                   |
| TotalReviews            | Total reviews                                                   |
| AverageRating           | Average rating                                                  |
| PositiveReviewPct       | Positive review percentage                                      |
| NegativeReviewPct       | Negative review percentage                                      |
| RecommendationPct       | Recommendation percentage                                       |
| TotalUnitsSold          | Total units sold                                                |
| TotalSalesValue         | Total sales value                                               |
| RecommendationRankScore | Calculated product recommendation score                         |
| RecommendationLevel     | Highly Recommended, Recommended, Average, or Low Recommendation |

## gold_customer_sentiment_trend

Tracks sentiment movement by month and review issue category.

| Column              | Description                    |
| ------------------- | ------------------------------ |
| ReviewMonth         | Review month                   |
| SentimentLabel      | Positive, Neutral, or Negative |
| ReviewIssueCategory | Review issue category          |
| ReviewCount         | Review count                   |
| AvgRating           | Average rating                 |

## gold_supply_chain_customer_risk

Identifies products with customer-facing supply chain risk.

| Column                 | Description                        |
| ---------------------- | ---------------------------------- |
| ProductID              | Product identifier                 |
| ProductName            | Product name                       |
| Category               | Product category                   |
| Brand                  | Product brand                      |
| SupplierID             | Supplier identifier                |
| ReturnCount            | Total return count                 |
| SupplyChainReturnCount | Supply chain-related return count  |
| ReviewCount            | Total review count                 |
| NegativeReviewCount    | Negative review count              |
| SupplyChainRiskScore   | Calculated supply chain risk score |
| SupplyChainRiskLevel   | Low, Medium, or High               |

---

# Future RAG Extension

Future RAG implementation can use policy and SOP documents such as:

* Return policy
* Refund policy
* Delivery policy
* Product warranty document
* Customer support SOP
* Supplier issue escalation SOP

These documents can be indexed using vector search and connected to Azure OpenAI to answer grounded business and customer support questions.

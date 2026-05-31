# Business Rules

## Project

Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform

## Scope

This project analyzes customer feedback, customer complaints, product reviews, payment issues, delivery issues, returns, and supply chain-related customer risks.

The current project uses rule-based PySpark classification, not a full RAG system.

## Data Quality Rules

### Customers

* CustomerID must not be null or blank.
* Duplicate customers are removed using CustomerID.
* Email values are converted to lowercase.
* SignupDate is converted to date format.

### Products

* ProductID must not be null or blank.
* UnitCost must be greater than or equal to zero.
* RetailPrice must be greater than or equal to zero.
* Currency must be EUR.
* Duplicate products are removed using ProductID.

### Orders

* OrderID must not be null or blank.
* CustomerID must not be null.
* GrossAmount, DiscountAmount, and NetAmount must be greater than or equal to zero.
* Currency must be EUR.
* Valid order statuses are Completed, Shipped, Cancelled, and Returned.
* Duplicate orders are removed using OrderID.

### Order Items

* OrderItemID must not be null or blank.
* OrderID and ProductID must not be null.
* Quantity must be greater than zero.
* UnitPrice and LineTotal must be greater than or equal to zero.
* Duplicate order items are removed using OrderItemID.

### Payments

* PaymentID must not be null or blank.
* OrderID must not be null.
* Amount must be greater than or equal to zero.
* Currency must be EUR.
* Valid payment statuses are Paid, Failed, Pending, and Refunded.
* PaymentIssueFlag is set to 1 when PaymentStatus is Failed.

### Shipments

* ShipmentID must not be null or blank.
* OrderID must not be null.
* Valid delivery statuses are Delivered, In Transit, Delayed, and Lost.
* DeliveryDelayDays is calculated when ActualDeliveryDate is available.
* DeliveryIssueFlag is set to 1 when DeliveryStatus is Delayed or Lost, or when DeliveryDelayDays is greater than zero.

### Returns

* ReturnID must not be null or blank.
* OrderID and ProductID must not be null.
* ReturnQty must be greater than zero.
* RefundAmount must be greater than or equal to zero.
* ReturnReason must not be null or blank.
* SupplyChainReturnFlag is set to 1 when the return reason is related to damaged product, wrong item, quality issue, or late delivery.

### Customer Reviews

* ReviewID must not be null or blank.
* OrderID, CustomerID, and ProductID must not be null.
* Rating must be between 1 and 5.
* ReviewText must not be null or blank.
* SentimentLabel is assigned based on Rating:

  * Rating 4 or 5 = Positive
  * Rating 3 = Neutral
  * Rating 1 or 2 = Negative
* NegativeFeedbackFlag is set to 1 when SentimentLabel is Negative.
* ReviewIssueCategory is classified using keywords from ReviewText.

### Support Tickets

* TicketID must not be null or blank.
* CustomerID and OrderID must not be null.
* IssueCategory must not be null or blank.
* Valid priorities are Low, Medium, High, and Critical.
* Valid statuses are Open, In Progress, Resolved, and Closed.
* ResolutionTimeHours must be null or greater than or equal to zero.
* IssueSeverityScore:

  * Critical = 4
  * High = 3
  * Medium = 2
  * Low = 1
* SupplyChainImpactFlag is set to 1 for Delivery Issue, Product Quality Issue, Wrong Item, and Refund Issue.
* PaymentLoginIssueFlag is set to 1 for Payment Issue and Login Issue.

### Chat Feedback

* ChatID must not be null or blank.
* CustomerID and OrderID must not be null.
* SatisfactionScore must be between 1 and 5.
* ChatSentimentLabel:

  * Score 4 or 5 = Positive
  * Score 3 = Neutral
  * Score 1 or 2 = Negative
* ChatIssueCategory is classified using keywords from Topic.

## Gold Layer Business Rules

### Product Feedback Summary

This table summarizes review performance by product.

Metrics include:

* TotalReviews
* AverageRating
* PositiveReviews
* NeutralReviews
* NegativeReviews
* RecommendedReviewCount
* PositiveReviewPct
* NegativeReviewPct
* RecommendationPct

### Customer Complaint Summary

This table combines customer master data, support tickets, reviews, and chat feedback.

CustomerRiskLevel rules:

* High Risk: CriticalTickets greater than 0 or NegativeReviews greater than or equal to 2
* Medium Risk: HighTickets greater than 0 or NegativeChats greater than or equal to 2
* Low Risk: all remaining customers

### Delivery Issue Analysis

This table analyzes delivery issues by country, carrier, and delivery status.

DeliveryRiskLevel rules:

* High: DeliveryIssuePct greater than or equal to 30
* Medium: DeliveryIssuePct greater than or equal to 15
* Low: below 15

### Payment and Login Issue Analysis

This table combines payment failure analysis and login support ticket analysis.

It helps identify checkout friction, failed payments, and account access issues.

### Return Reason Analysis

This table analyzes return reasons by product category and brand.

ReturnRiskLevel rules:

* High: SupplyChainRelatedReturns greater than or equal to 10
* Medium: SupplyChainRelatedReturns greater than or equal to 5
* Low: below 5

### Product Recommendation Ranking

This table ranks products using:

* AverageRating
* RecommendationPct
* PositiveReviewPct
* NegativeReviewPct
* Units sold
* Sales value

RecommendationLevel rules:

* Highly Recommended: RecommendationRankScore greater than or equal to 100
* Recommended: RecommendationRankScore greater than or equal to 70
* Average: RecommendationRankScore greater than or equal to 40
* Low Recommendation: below 40

### Customer Sentiment Trend

This table summarizes review sentiment by month and issue category.

### Supply Chain Customer Risk

This table identifies products with customer-facing supply chain risk.

SupplyChainRiskScore formula:

```text
SupplyChainRiskScore = SupplyChainReturnCount * 3 + NegativeReviewCount * 2
```

SupplyChainRiskLevel rules:

* High: score greater than or equal to 20
* Medium: score greater than or equal to 10
* Low: below 10

## Future Enhancement Rules

Future RAG implementation may use:

* Return policy documents
* Delivery policy documents
* Refund policy documents
* Product warranty documents
* Support SOP documents
* Vector search
* Azure OpenAI
* Grounded answer generation

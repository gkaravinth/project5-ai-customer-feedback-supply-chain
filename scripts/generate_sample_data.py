"""
Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform
Script: generate_sample_data.py

Purpose:
Generate realistic e-commerce customer, order, payment, shipment, return,
review, support ticket, and chat feedback source files.

Output:
data/source_files/
"""

import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

random.seed(55)

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "data" / "source_files"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

START_DATE = datetime(2026, 5, 1)
END_DATE = datetime(2026, 5, 25)
CURRENCY = "EUR"


# ============================================================
# Helper functions
# ============================================================

def write_csv(file_name, fieldnames, rows):
    file_path = OUTPUT_DIR / file_name
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created CSV: {file_path}")


def write_json(file_name, data):
    file_path = OUTPUT_DIR / file_name
    with open(file_path, mode="w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"Created JSON: {file_path}")


def random_date(start_date, end_date):
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    random_seconds = random.randint(0, 86399)
    return start_date + timedelta(days=random_days, seconds=random_seconds)


def date_str(date_value):
    return date_value.strftime("%Y-%m-%d")


def datetime_str(date_value):
    return date_value.strftime("%Y-%m-%d %H:%M:%S")


# ============================================================
# Master data
# ============================================================

product_categories = {
    "Footwear": ["Running Shoes", "Training Shoes", "Lifestyle Sneakers"],
    "Apparel": ["T-Shirt", "Hoodie", "Jacket", "Shorts"],
    "Accessories": ["Backpack", "Water Bottle", "Cap", "Gym Bag"],
    "Equipment": ["Yoga Mat", "Resistance Band", "Dumbbell Set"],
    "Kidswear": ["Kids T-Shirt", "Kids Hoodie", "Kids Shoes"]
}

brands = ["EuroSport", "UrbanAthlete", "PeakMotion", "NordRun", "AdlerFit"]
supplier_ids = [f"SUP{i:03d}" for i in range(1, 9)]


customers = []
for i in range(1, 501):
    customers.append({
        "CustomerID": f"CUST{i:06d}",
        "CustomerName": random.choice([
            "Anna Muller", "Lucas Schmidt", "Sofia Rossi", "Emma Dubois",
            "Jan Kowalski", "Mila Novak", "Liam Weber", "Noah Martin",
            "Olivia Hansen", "Ella Fischer"
        ]),
        "Email": f"customer{i}@example.com",
        "Country": random.choice(["Germany", "France", "Italy", "Netherlands", "Spain", "Sweden", "Belgium", "Austria"]),
        "City": random.choice(["Berlin", "Paris", "Milan", "Amsterdam", "Madrid", "Stockholm", "Brussels", "Vienna"]),
        "SignupDate": date_str(random_date(datetime(2024, 1, 1), START_DATE)),
        "CustomerSegment": random.choice(["Standard", "Silver", "Gold", "VIP"]),
        "IsActive": True
    })

products = []
product_counter = 1

for category, subcategories in product_categories.items():
    for _ in range(20):
        product_id = f"P{product_counter:04d}"
        subcategory = random.choice(subcategories)
        brand = random.choice(brands)
        unit_cost = round(random.uniform(5, 90), 2)
        retail_price = round(unit_cost * random.uniform(1.4, 2.6), 2)

        products.append({
            "ProductID": product_id,
            "SKU": f"SKU-{product_counter:05d}",
            "ProductName": f"{brand} {subcategory}",
            "Category": category,
            "SubCategory": subcategory,
            "Brand": brand,
            "SupplierID": random.choice(supplier_ids),
            "UnitCost": unit_cost,
            "RetailPrice": retail_price,
            "Currency": CURRENCY,
            "IsActive": True
        })

        product_counter += 1

products = products[:100]

# Intentional bad product record
products.append({
    "ProductID": "",
    "SKU": "SKU-BAD-001",
    "ProductName": "Invalid Missing Product",
    "Category": "",
    "SubCategory": "Unknown",
    "Brand": "Unknown",
    "SupplierID": "SUP999",
    "UnitCost": -20,
    "RetailPrice": 10,
    "Currency": "USD",
    "IsActive": True
})


# ============================================================
# Orders and order items
# ============================================================

orders = []
order_items = []
order_ids = []

for i in range(1, 1201):
    order_id = f"ORD{i:06d}"
    order_ids.append(order_id)

    customer = random.choice(customers)
    order_date = random_date(START_DATE, END_DATE)
    order_status = random.choice(["Completed", "Completed", "Completed", "Shipped", "Cancelled", "Returned"])

    item_count = random.randint(1, 4)
    selected_products = random.sample(products[:100], item_count)

    order_gross = 0

    for line_no, product in enumerate(selected_products, start=1):
        quantity = random.randint(1, 4)
        unit_price = float(product["RetailPrice"])
        line_total = round(quantity * unit_price, 2)
        order_gross += line_total

        order_items.append({
            "OrderItemID": f"OI{i:06d}_{line_no}",
            "OrderID": order_id,
            "ProductID": product["ProductID"],
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "LineTotal": line_total
        })

    discount = round(order_gross * random.choice([0, 0, 0.05, 0.10, 0.15]), 2)
    net_amount = round(order_gross - discount, 2)

    orders.append({
        "OrderID": order_id,
        "CustomerID": customer["CustomerID"],
        "OrderDate": datetime_str(order_date),
        "OrderStatus": order_status,
        "SalesChannel": random.choice(["Website", "Mobile App"]),
        "GrossAmount": round(order_gross, 2),
        "DiscountAmount": discount,
        "NetAmount": net_amount,
        "Currency": CURRENCY
    })

# Intentional bad order
orders.append({
    "OrderID": "ORD_BAD_001",
    "CustomerID": "CUST999999",
    "OrderDate": "2026-07-01 10:00:00",
    "OrderStatus": "UnknownStatus",
    "SalesChannel": "Website",
    "GrossAmount": -100,
    "DiscountAmount": 200,
    "NetAmount": -300,
    "Currency": "USD"
})


# ============================================================
# Payments
# ============================================================

payments = []

for order in orders[:-1]:
    payment_status = random.choice(["Paid", "Paid", "Paid", "Failed", "Pending", "Refunded"])
    payments.append({
        "PaymentID": f"PAY{len(payments) + 1:06d}",
        "OrderID": order["OrderID"],
        "PaymentDate": order["OrderDate"],
        "PaymentMethod": random.choice(["Card", "PayPal", "Wallet", "Bank Transfer"]),
        "PaymentStatus": payment_status,
        "PaymentFailureReason": random.choice(["", "", "", "Card Declined", "3DS Failed", "Gateway Timeout"]) if payment_status == "Failed" else "",
        "Amount": order["NetAmount"],
        "Currency": order["Currency"]
    })

payments.append({
    "PaymentID": "PAY_BAD_001",
    "OrderID": "ORD999999",
    "PaymentDate": "2026-07-01 12:00:00",
    "PaymentMethod": "Unknown",
    "PaymentStatus": "InvalidStatus",
    "PaymentFailureReason": "Unknown",
    "Amount": -50,
    "Currency": "USD"
})


# ============================================================
# Shipments
# ============================================================

shipments = []

for order in orders[:-1]:
    order_date = datetime.strptime(order["OrderDate"], "%Y-%m-%d %H:%M:%S")
    expected_delivery = order_date + timedelta(days=random.randint(2, 7))

    delivery_status = random.choice(["Delivered", "Delivered", "Delivered", "In Transit", "Delayed", "Lost"])
    actual_delivery = ""
    if delivery_status == "Delivered":
        actual_delivery = date_str(expected_delivery + timedelta(days=random.randint(-1, 4)))

    shipments.append({
        "ShipmentID": f"SHP{len(shipments) + 1:06d}",
        "OrderID": order["OrderID"],
        "WarehouseID": "W001",
        "Carrier": random.choice(["DHL", "DPD", "UPS", "FedEx", "PostNL"]),
        "ShipmentDate": date_str(order_date + timedelta(days=1)),
        "ExpectedDeliveryDate": date_str(expected_delivery),
        "ActualDeliveryDate": actual_delivery,
        "DeliveryStatus": delivery_status,
        "DeliveryCountry": random.choice(["Germany", "France", "Italy", "Netherlands", "Spain", "Sweden", "Belgium", "Austria"])
    })

shipments.append({
    "ShipmentID": "SHP_BAD_001",
    "OrderID": "ORD999999",
    "WarehouseID": "W999",
    "Carrier": "Unknown",
    "ShipmentDate": "2026-06-10",
    "ExpectedDeliveryDate": "2026-05-01",
    "ActualDeliveryDate": "2026-04-30",
    "DeliveryStatus": "InvalidStatus",
    "DeliveryCountry": ""
})


# ============================================================
# Returns
# ============================================================

returns = []

return_reasons = [
    "Size issue",
    "Damaged product",
    "Wrong item received",
    "Quality issue",
    "Customer changed mind",
    "Late delivery",
    "Refund requested"
]

for i in range(1, 301):
    order_item = random.choice(order_items)
    refund_amount = round(float(order_item["LineTotal"]) * random.uniform(0.5, 1.0), 2)

    returns.append({
        "ReturnID": f"RET{i:06d}",
        "OrderID": order_item["OrderID"],
        "ProductID": order_item["ProductID"],
        "ReturnDate": date_str(random_date(START_DATE, END_DATE + timedelta(days=5))),
        "ReturnQty": random.randint(1, max(1, int(order_item["Quantity"]))),
        "ReturnReason": random.choice(return_reasons),
        "RefundAmount": refund_amount
    })

returns.append({
    "ReturnID": "RET_BAD_001",
    "OrderID": "ORD999999",
    "ProductID": "P9999",
    "ReturnDate": "2026-07-01",
    "ReturnQty": -1,
    "ReturnReason": "",
    "RefundAmount": -100
})


# ============================================================
# Customer reviews
# ============================================================

positive_reviews = [
    "Excellent quality and fast delivery. I highly recommend this product.",
    "Very comfortable and worth the price. I will buy again.",
    "Great product, good packaging, and smooth ordering experience.",
    "The product quality is better than expected.",
    "Perfect fit and very useful for training."
]

neutral_reviews = [
    "Product is okay, but delivery took a little longer.",
    "Average quality, not bad but not excellent.",
    "The product is fine, but packaging can be improved.",
    "Good product, but the size guide was confusing.",
    "It works as expected."
]

negative_reviews = [
    "Poor quality and the item arrived damaged.",
    "Delivery was very late and customer support was slow.",
    "Payment failed twice and the order process was frustrating.",
    "Wrong item received and return process was difficult.",
    "The product is not worth the price."
]

customer_reviews = []

for i in range(1, 701):
    order = random.choice(orders[:-1])
    product = random.choice(products[:100])
    review_type = random.choice(["positive", "positive", "neutral", "negative"])

    if review_type == "positive":
        rating = random.choice([4, 5])
        text = random.choice(positive_reviews)
        recommend = True
    elif review_type == "neutral":
        rating = 3
        text = random.choice(neutral_reviews)
        recommend = random.choice([True, False])
    else:
        rating = random.choice([1, 2])
        text = random.choice(negative_reviews)
        recommend = False

    customer_reviews.append({
        "ReviewID": f"REV{i:06d}",
        "OrderID": order["OrderID"],
        "CustomerID": order["CustomerID"],
        "ProductID": product["ProductID"],
        "ReviewDate": date_str(random_date(START_DATE, END_DATE + timedelta(days=5))),
        "Rating": rating,
        "ReviewText": text,
        "RecommendationFlag": recommend
    })

customer_reviews.append({
    "ReviewID": "REV_BAD_001",
    "OrderID": "ORD999999",
    "CustomerID": "CUST999999",
    "ProductID": "P9999",
    "ReviewDate": "2026-07-01",
    "Rating": 10,
    "ReviewText": "",
    "RecommendationFlag": False
})


# ============================================================
# Support tickets
# ============================================================

ticket_templates = {
    "Login Issue": [
        "I cannot login to my account.",
        "Password reset email is not arriving.",
        "My account is locked after multiple attempts."
    ],
    "Payment Issue": [
        "Payment failed during checkout.",
        "My card was charged but order was not created.",
        "Payment gateway timed out."
    ],
    "Delivery Issue": [
        "My order delivery is delayed.",
        "Tracking shows delivered but I did not receive the parcel.",
        "Carrier has not updated shipment status."
    ],
    "Product Quality Issue": [
        "The product arrived damaged.",
        "The item quality is poor.",
        "The stitching came loose after first use."
    ],
    "Wrong Item": [
        "I received the wrong item.",
        "The color and size are different from what I ordered.",
        "The product code does not match my order."
    ],
    "Refund Issue": [
        "Refund is delayed.",
        "I returned the item but refund is not processed.",
        "Refund amount is incorrect."
    ]
}

support_tickets = []

for i in range(1, 501):
    order = random.choice(orders[:-1])
    category = random.choice(list(ticket_templates.keys()))
    created = random_date(START_DATE, END_DATE + timedelta(days=5))
    priority = random.choice(["Low", "Medium", "High", "Critical"])

    support_tickets.append({
        "TicketID": f"TIC{i:06d}",
        "CustomerID": order["CustomerID"],
        "OrderID": order["OrderID"],
        "TicketDate": datetime_str(created),
        "IssueCategory": category,
        "TicketText": random.choice(ticket_templates[category]),
        "Priority": priority,
        "Status": random.choice(["Open", "In Progress", "Resolved", "Closed"]),
        "ResolutionTimeHours": random.choice([2, 4, 8, 12, 24, 48, 72, None])
    })

support_tickets.append({
    "TicketID": "TIC_BAD_001",
    "CustomerID": "",
    "OrderID": "ORD999999",
    "TicketDate": "2026-07-01 10:00:00",
    "IssueCategory": "",
    "TicketText": "",
    "Priority": "Unknown",
    "Status": "InvalidStatus",
    "ResolutionTimeHours": -5
})


# ============================================================
# Chat feedback nested JSON
# ============================================================

chat_feedback = []

for i in range(1, 251):
    customer = random.choice(customers)
    order = random.choice(orders[:-1])
    topic = random.choice([
        "login problem", "payment failed", "late delivery",
        "damaged product", "refund delay", "wrong item",
        "positive product feedback", "stock availability"
    ])

    messages = [
        {
            "sender": "customer",
            "message_time": datetime_str(random_date(START_DATE, END_DATE)),
            "message_text": f"I need help with {topic}."
        },
        {
            "sender": "agent",
            "message_time": datetime_str(random_date(START_DATE, END_DATE)),
            "message_text": "Thank you for contacting support. We will check this for you."
        }
    ]

    chat_feedback.append({
        "chat_id": f"CHAT{i:06d}",
        "customer": {
            "customer_id": customer["CustomerID"],
            "customer_name": customer["CustomerName"],
            "country": customer["Country"]
        },
        "order_id": order["OrderID"],
        "chat_date": datetime_str(random_date(START_DATE, END_DATE)),
        "topic": topic,
        "satisfaction_score": random.choice([1, 2, 3, 4, 5]),
        "messages": messages
    })

chat_feedback.append({
    "chat_id": "",
    "customer": {
        "customer_id": "",
        "customer_name": "Invalid Customer",
        "country": ""
    },
    "order_id": "ORD999999",
    "chat_date": "2026-07-01 10:00:00",
    "topic": "",
    "satisfaction_score": 10,
    "messages": []
})


# ============================================================
# Write files
# ============================================================

write_csv("customers.csv", list(customers[0].keys()), customers)
write_csv("products.csv", list(products[0].keys()), products)
write_csv("orders.csv", list(orders[0].keys()), orders)
write_csv("order_items.csv", list(order_items[0].keys()), order_items)
write_csv("payments.csv", list(payments[0].keys()), payments)
write_csv("shipments.csv", list(shipments[0].keys()), shipments)
write_csv("returns.csv", list(returns[0].keys()), returns)
write_csv("customer_reviews.csv", list(customer_reviews[0].keys()), customer_reviews)
write_csv("support_tickets.csv", list(support_tickets[0].keys()), support_tickets)
write_json("chat_feedback.json", chat_feedback)

print("\nProject 5 sample source files generated successfully.")
print(f"Output folder: {OUTPUT_DIR}")
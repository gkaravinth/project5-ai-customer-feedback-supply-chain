"""
Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform
Script: profile_source_data.py

Purpose:
Profile generated source files and print row counts, column counts,
column names, and sample nested JSON structure.

Output:
Console profiling summary.
"""

import csv
import json
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = BASE_DIR / "data" / "source_files"


CSV_FILES = [
    "customers.csv",
    "products.csv",
    "orders.csv",
    "order_items.csv",
    "payments.csv",
    "shipments.csv",
    "returns.csv",
    "customer_reviews.csv",
    "support_tickets.csv",
]

JSON_FILES = [
    "chat_feedback.json",
]


# ============================================================
# Helper functions
# ============================================================

def profile_csv(file_name: str) -> None:
    file_path = SOURCE_DIR / file_name

    if not file_path.exists():
        print(f"\nCSV File Missing: {file_name}")
        return

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        columns = reader.fieldnames or []

    print(f"\nCSV File: {file_name}")
    print(f"Rows: {len(rows)}")
    print(f"Columns: {len(columns)}")
    print(f"Column Names: {columns}")

    if rows:
        print(f"Sample Row: {rows[0]}")


def profile_json(file_name: str) -> None:
    file_path = SOURCE_DIR / file_name

    if not file_path.exists():
        print(f"\nJSON File Missing: {file_name}")
        return

    with open(file_path, mode="r", encoding="utf-8") as file:
        data = json.load(file)

    print(f"\nJSON File: {file_name}")

    if isinstance(data, list):
        print(f"Records: {len(data)}")

        if data:
            first_record = data[0]
            print(f"Top-level fields: {list(first_record.keys())}")

            customer = first_record.get("customer", {})
            messages = first_record.get("messages", [])

            if isinstance(customer, dict):
                print(f"Customer fields: {list(customer.keys())}")

            if isinstance(messages, list) and messages:
                print(f"Message fields: {list(messages[0].keys())}")
                print(f"Message count in first record: {len(messages)}")

            print(f"Sample Record: {first_record}")
    else:
        print("JSON root is not a list.")
        print(f"Type: {type(data)}")


# ============================================================
# Main profiling execution
# ============================================================

def main() -> None:
    print("Project 5 Source Data Profiling Started")
    print(f"Source folder: {SOURCE_DIR}")

    for csv_file in CSV_FILES:
        profile_csv(csv_file)

    for json_file in JSON_FILES:
        profile_json(json_file)

    print("\nProject 5 source data profiling completed successfully.")


if __name__ == "__main__":
    main()
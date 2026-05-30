# Azure Upload Summary

## Project

Project 5 - AI Customer Feedback & Supply Chain Intelligence Platform

## Storage Account

europedata

## Container

project5-customer-feedback-platform

## Folder Structure

The Azure Storage container was created with the following data lake style folders:

- landing
- raw
- processed
- archive
- rejected

## Landing Zone Upload

The generated Project 5 source files were uploaded into the landing zone.

Landing path:

```text
project5-customer-feedback-platform/landing/

Uploaded Source Files
customers.csv
products.csv
orders.csv
order_items.csv
payments.csv
shipments.csv
returns.csv
customer_reviews.csv
support_tickets.csv
chat_feedback.json
Purpose

The landing zone stores the initial source files before Azure Data Factory validates and copies them into the raw zone.

Next Step

Build Azure Data Factory pipeline to:

Validate required landing files.
Copy valid files from landing to raw.
Prepare raw files for Databricks Bronze ingestion.



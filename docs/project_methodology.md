# Project Methodology

## 1. Objective

Turn raw online retail transaction records into a clean, queryable sales dataset and use it to answer practical business questions.

## 2. Source

UCI Machine Learning Repository, dataset 352: Online Retail. The source contains 541,909 rows and eight fields describing invoice lines between 1 December 2010 and 9 December 2011. See the source page and citation in the root README.

## 3. Extract

The extraction step uses the `ucimlrepo` Python package to retrieve dataset 352 and stores a local copy in `data/raw/online_retail.xlsx`. The source is not edited.

## 4. Transform

The transformation step:
- validates the expected columns;
- removes exact duplicate rows;
- trims text fields and normalizes invoice number casing;
- parses invoice timestamps;
- converts quantity, unit price, and customer identifier to suitable types;
- identifies cancellation invoices (invoice number starts with C);
- excludes cancellation rows, invalid timestamps, non-positive quantities, and non-positive prices from completed-sales KPIs;
- retains missing customer IDs in overall sales totals, while excluding them from customer-specific rankings;
- fills missing product descriptions and country labels with explicit placeholders;
- calculates line revenue as quantity multiplied by unit price.

The script emits counts for key quality issues so exclusions are visible rather than silent.

## 5. Load

The transformed dataset is loaded to:
- a CSV file for portability;
- a SQLite database table named `sales`;
- a quality-summary table named `data_quality_summary`.

SQLite makes it possible to demonstrate SQL aggregation without requiring a separate database server.

## 6. Analyze

SQL queries calculate monthly revenue, revenue by country, top products, and top customers. Python calculates headline KPIs and creates charts for monthly revenue, country revenue, product revenue, and weekday revenue.

## 7. Interpretation cautions

Revenue is not profit. Unit cost, shipping, tax, discounts, and payment status are not available as a complete accounting model. Customer-level findings exclude transactions without a CustomerID. The dataset covers only one retailer and roughly one year; seasonal conclusions should therefore be treated cautiously.

## 8. Reproducibility

Install `requirements.txt` and run `python -m src.run_pipeline`. Generated datasets and outputs are intentionally excluded from Git to keep the repository lightweight; they can be recreated from the source dataset.

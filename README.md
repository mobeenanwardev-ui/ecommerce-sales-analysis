# E-Commerce Sales Analysis

A reproducible end-to-end data analytics project using the **UCI Online Retail** transaction dataset. The project demonstrates data extraction, data quality assessment, cleaning, ETL, SQL loading, exploratory analysis, business KPI calculation, and visualisation.

## Business context

The dataset contains transactions from a UK-based online retailer selling giftware. The records cover **1 December 2010 to 9 December 2011** and include invoice, product, quantity, price, customer, timestamp, and country information.

**Business question:** What can transaction history tell us about revenue patterns, products, customers, and geographic performance?

## Questions explored

1. How does revenue change over time?
2. Which products generate the most revenue?
3. Which countries contribute the most revenue?
4. Which customers have the highest recorded spend?
5. How do order volume and average order value change?
6. What data-quality issues must be handled before drawing conclusions?

## Technology

- Python 3.10+
- pandas and NumPy for data preparation
- SQLite for the load/warehouse step and SQL analysis
- Matplotlib and Seaborn for charts
- UCI Machine Learning Repository via `ucimlrepo`

## ETL architecture

```text
UCI Online Retail dataset
        |
        v
Extract (src/extract.py)
        |
        v
Raw data snapshot (data/raw/)
        |
        v
Transform + quality checks (src/transform.py)
        |
        +----> Cleaned CSV (data/processed/)
        |
        v
Load to SQLite (src/load.py)
        |
        v
Analysis + charts (src/analyze.py)
        |
        +----> outputs/figures/
        +----> outputs/reports/
```

## Data handling decisions

- Preserve the original source file in `data/raw/`; do not edit it manually.
- Parse invoice timestamps into a real datetime type.
- Treat invoice numbers beginning with `C` as cancellation/return records and keep them out of completed-sales KPIs.
- Exclude non-positive quantities and non-positive unit prices from the completed-sales fact table; report how many rows are excluded.
- Do not discard transactions with an unknown CustomerID from overall sales analysis. Exclude them only from customer-level analysis, where a customer identifier is essential.
- Remove exact duplicate transaction lines.
- Calculate line revenue as `Quantity × UnitPrice`.
- Keep currency in the source unit, GBP (£); this dataset does not provide an exchange-rate table.

These are analytical rules, not claims about the retailer's accounting system. The project reports the rules transparently so results can be interpreted correctly.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the full pipeline:

   ```bash
   python -m src.run_pipeline
   ```

The first run downloads the dataset through the UCI repository package. Generated raw and processed data, SQLite database, reports, and charts are written to folders excluded from Git where appropriate.

## Repository structure

```text
.
├── data/
│   ├── raw/                 # downloaded source file (not committed)
│   └── processed/           # cleaned data (not committed)
├── docs/
│   └── project_methodology.md
├── outputs/
│   ├── figures/             # generated charts
│   └── reports/             # generated KPI and quality reports
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── analyze.py
│   └── run_pipeline.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Dataset attribution

Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33

Dataset page: https://archive.ics.uci.edu/dataset/352/online+retail  
License: **CC BY 4.0**. Attribution is provided here; consult the source page for the complete license terms.

## Important limitations

- The data covers approximately one year, so it is not sufficient to establish long-term trends or seasonality over multiple years.
- The dataset represents one retailer and should not be generalized to all e-commerce businesses.
- Missing customer identifiers limit customer-level analysis.
- Revenue is calculated from recorded quantities and unit prices; it is not necessarily equal to recognized accounting revenue or profit. No cost-of-goods data is supplied, so profit is not calculated.

## Author

Mobeen Anwar — M.Sc. High Integrity Systems, Frankfurt University of Applied Sciences.

This repository is a portfolio project. All findings will be generated from the published data-processing rules and scripts; see the reports and figures after running the pipeline.

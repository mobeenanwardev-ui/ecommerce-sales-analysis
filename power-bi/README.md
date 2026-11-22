# Power BI — Online Retail Sales & Business Performance

A beginner-friendly Power BI extension to the repository's Python e-commerce analysis. It uses the same UCI Online Retail dataset so both projects tell one consistent business story.

## Business questions
- How much revenue and how many orders were recorded?
- How does revenue change over time?
- Which countries and products contribute most to revenue?
- What is the average order value?
- How many unique customers are represented?

## Dataset
UCI Machine Learning Repository — Online Retail (Chen, 2015), dataset 352, CC BY 4.0.
- https://archive.ics.uci.edu/dataset/352/online+retail
- https://doi.org/10.24432/C5BW33

Download the Excel workbook and save it locally as Online Retail.xlsx. Do not commit the raw workbook unless you intentionally want to store the full dataset in Git.

## Project files
- POWER_QUERY.md — import and cleaning steps
- DAX_MEASURES.dax — measures and date table expressions
- PROJECT_GUIDE.md — dashboard build guide and interview notes
- DATA_DICTIONARY.md — fields, KPIs, and analytical decisions
- theme.json — report theme

## Build status
This folder currently contains the report source assets and build instructions. A genuine PBIX report must be created and saved using Power BI Desktop on Windows. Power BI Desktop is not a native macOS application, so this repository does not claim that a PBIX has already been generated or tested.

Follow PROJECT_GUIDE.md to build the report. Once saved, add the PBIX file and dashboard screenshots to this folder.

## Recommended report pages
1. Sales Overview — revenue, orders, units, customers, monthly trend.
2. Product Performance — top products by revenue and quantity.
3. Geographic Performance — revenue and orders by country.

## Scope
This is descriptive analytics, not financial accounting. The source dataset does not contain product costs, so profit and margin cannot be calculated reliably.

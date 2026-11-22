# Data dictionary and analytical decisions

## Source
UCI Machine Learning Repository — Online Retail, dataset 352. Chen (2015). CC BY 4.0.
https://archive.ics.uci.edu/dataset/352/online+retail

The dataset contains transaction-line records from a UK-based online retailer, covering December 2010 through December 2011.

## Main fields

| Field | Meaning | Power BI type |
|---|---|---|
| InvoiceNo | Invoice identifier; values beginning with C indicate cancellations | Text |
| StockCode | Product/item identifier | Text |
| Description | Product description | Text |
| Quantity | Number of units in the transaction line | Whole number |
| InvoiceDate | Date and time of transaction | Date/Time |
| UnitPrice | Unit price in GBP | Currency |
| CustomerID | Customer identifier; may be missing | Text |
| Country | Customer country | Text |
| Revenue | Quantity multiplied by UnitPrice | Currency |

## Cleaning decisions
1. Remove exact duplicate rows.
2. Exclude cancelled invoices whose InvoiceNo starts with C.
3. Exclude rows with Quantity <= 0.
4. Exclude rows with UnitPrice <= 0.
5. Keep transactions with blank CustomerID in overall revenue and order analysis.
6. Exclude blank CustomerID only from the unique-customer count.
7. Calculate Revenue = Quantity × UnitPrice.

## KPI definitions
- Total Revenue: sum of Revenue.
- Total Orders: distinct count of InvoiceNo.
- Total Units Sold: sum of Quantity.
- Unique Customers: distinct non-blank CustomerID count.
- Average Order Value: Total Revenue divided by Total Orders.
- Revenue per Customer: Total Revenue divided by Unique Customers.

## Limitations
- No cost-of-goods-sold field is available. Do not report profit or profit margin.
- Revenue is in GBP, not EUR.
- The data represents one retailer and a limited historical period.
- InvoiceNo is used as the order identifier in this project.
- Missing CustomerID values mean customer-level metrics do not cover every transaction.

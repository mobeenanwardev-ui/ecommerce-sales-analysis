# Power BI project guide — Sales & Business Performance

This guide explains the business problem, report build, and how to discuss the project in a Werkstudent interview.

## 1. Project objective
Build an interactive report that helps a retail business understand sales performance across time, products, and countries. This is descriptive analytics, not forecasting.

## 2. Tools
- Microsoft Power BI Desktop
- Power Query for data cleaning
- DAX for measures and date calculations
- UCI Online Retail dataset

## 3. Build the report

### Step A — Load and clean
1. Download the UCI Online Retail Excel workbook.
2. Import it into Power BI Desktop.
3. Open Transform Data.
4. Follow POWER_QUERY.md.
5. Confirm the query is named OnlineRetail.
6. Close & Apply.

### Step B — Create the data model
1. Create DateTable using the expression in DAX_MEASURES.dax (New Table).
2. Add Year, Month Number, Month, and Year-Month calculated columns.
3. Create the relationship DateTable[Date] → OnlineRetail[InvoiceDate_Date].
4. Mark DateTable as the date table.
5. Sort DateTable[Month] by DateTable[Month Number].

### Step C — Create measures
Copy the measures from DAX_MEASURES.dax into Power BI one at a time using New Measure. Create the date table separately as a New Table and date attributes as calculated columns.

Formatting:
- Total Revenue, Average Order Value, Revenue per Customer: GBP currency (£).
- Total Orders, Total Units Sold, Unique Customers: whole number.
- Average Selling Price: GBP currency (£).

### Step D — Design the pages

#### Page 1: Sales Overview
KPI cards: Total Revenue, Total Orders, Total Units Sold, Unique Customers.
- Line chart: DateTable[Year-Month] on X-axis; Total Revenue on Y-axis.
- Bar chart: Country and Total Revenue, filtered to Top 10 countries by revenue.
- Slicers: DateTable[Year], Country.

#### Page 2: Product Performance
- Bar chart: Description and Total Revenue, Top 10 products.
- Bar chart: Description and Total Units Sold, Top 10 products.
- Table: Description, Total Revenue, Total Units Sold.
- Slicers: Year, Country.

#### Page 3: Geographic Performance
- Bar chart: Country and Total Revenue.
- Cards: Total Revenue, Total Orders, Unique Customers.
- Table: Country, Total Revenue, Total Orders, Unique Customers.
- Slicer: Country.

Use a consistent light background, restrained accent colors, readable labels, and meaningful titles. Avoid 3D charts and excessive visual clutter. Apply theme.json through View → Themes → Browse for themes.

### Step E — Save and capture
1. Save as Online_Retail_Sales_Analytics.pbix.
2. Capture screenshots of each report page.
3. Add the PBIX and screenshots to this folder in GitHub.
4. Update the project README only after the report has been built and checked in Power BI Desktop.

## 4. Business value
The report helps a manager understand revenue trends, leading countries, high-performing products, order volume, and average order value. Slicers allow interactive exploration by date and country.

Do not claim that a country or product is profitable: the dataset does not include product costs.

## 5. Interview explanation
"I used the UCI Online Retail transaction dataset to build a Power BI sales performance report. I cleaned the transaction data in Power Query by removing duplicates, cancelled invoices, and invalid quantity or price records. I created a date table and connected it to the transaction table. Then I wrote DAX measures for revenue, orders, units sold, unique customers, and average order value. The report has pages for overall sales, product performance, and geographic performance. It allows users to filter results by date and country and identify the main sales trends."

## 6. Interview questions

**Why did you use Power Query?**  
To clean and prepare raw transaction data before loading it into the model.

**Why is InvoiceNo text?**  
It is an identifier, not a number to calculate with. It can also contain cancellation prefixes.

**Why use DISTINCTCOUNT for orders?**  
The dataset has one row per transaction line. An invoice can contain multiple products, so counting rows would overcount orders.

**What is DAX?**  
Data Analysis Expressions, the formula language used to create calculations in Power BI.

**Why create a date table?**  
It provides a dedicated calendar dimension for filtering and time-based analysis.

**What is a relationship?**  
A model connection that lets a filter from one table, such as DateTable, filter related rows in another table.

**Can you calculate profit?**  
No. The dataset does not provide product costs, so reliable profit cannot be calculated.

**What is average order value?**  
Total revenue divided by the number of distinct invoices in the current filter context.

**What does a slicer do?**  
It lets a report user filter visuals interactively, for example by year or country.

## 7. Limitations and honest presentation
This is a beginner-level portfolio project. The report uses historical data from one retailer, not live business data. It is descriptive, not a production BI solution. Be prepared to explain the cleaning rules, data model, DAX measures, and limitations.

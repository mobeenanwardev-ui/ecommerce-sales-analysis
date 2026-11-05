# E-Commerce Sales Analysis

A beginner-friendly data analytics project built in **one Jupyter Notebook** using Python and the UCI Online Retail dataset.

## Project goal

Analyse historical online retail transactions to understand sales performance and answer practical business questions:

- How does revenue change month by month?
- Which products generate the most revenue?
- Which countries contribute the most revenue?
- Which customers have the highest recorded spend?
- What is the average order value?

## Tools used

- Python
- Jupyter Notebook
- pandas and NumPy
- Matplotlib and Seaborn

## Notebook

Open **[`notebooks/ECommerce_Sales_Analysis.ipynb`](notebooks/ECommerce_Sales_Analysis.ipynb)** to follow the complete analysis from beginning to end. It is intentionally kept in one notebook with simple, sequential steps and explanations.

## How to run

1. Download or clone this repository.
2. Install the packages:

   ```bash
   pip install pandas numpy matplotlib seaborn ucimlrepo openpyxl jupyter
   ```

3. Start Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

4. Open `notebooks/ECommerce_Sales_Analysis.ipynb` and run the cells from top to bottom.

The notebook downloads dataset 352 from UCI when the data-loading cell runs. Internet access is needed for the first download.

## Data source

Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33

Dataset page: https://archive.ics.uci.edu/dataset/352/online+retail  
License: CC BY 4.0. The original dataset is attributed to UCI.

## Important analytical decisions

- Exact duplicate rows are removed.
- Cancellation invoices (invoice numbers beginning with `C`) are excluded from completed-sales analysis.
- Rows with non-positive quantity or unit price are excluded from completed-sales analysis.
- Transactions with missing CustomerID remain in overall sales totals; they are excluded only from customer-level analysis.
- Revenue is calculated as `Quantity × UnitPrice`.
- Revenue is not profit. The dataset does not provide product costs.

## Project limitations

The data represents one retailer and approximately one year of activity. It should not be treated as a complete accounting dataset or as evidence about every e-commerce business.

## Author

Mobeen Anwar — M.Sc. High Integrity Systems, Frankfurt University of Applied Sciences.

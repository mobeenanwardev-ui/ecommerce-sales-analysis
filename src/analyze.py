"""Create business summaries, SQL examples, and charts from the SQLite sales table."""
from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "outputs" / "ecommerce_sales.db"
FIG_DIR = ROOT / "outputs" / "figures"
REPORT_DIR = ROOT / "outputs" / "reports"

def analyze() -> dict:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    with sqlite3.connect(DB_PATH) as conn:
        sales = pd.read_sql_query("SELECT * FROM sales", conn, parse_dates=["InvoiceDate"])
        monthly = pd.read_sql_query("""
            SELECT InvoiceMonth, ROUND(SUM(Revenue), 2) AS revenue,
                   COUNT(DISTINCT InvoiceNo) AS orders
            FROM sales GROUP BY InvoiceMonth ORDER BY InvoiceMonth
        """, conn)
        countries = pd.read_sql_query("""
            SELECT Country, ROUND(SUM(Revenue), 2) AS revenue
            FROM sales GROUP BY Country ORDER BY revenue DESC LIMIT 10
        """, conn)
        products = pd.read_sql_query("""
            SELECT StockCode, Description, ROUND(SUM(Revenue), 2) AS revenue,
                   SUM(Quantity) AS units
            FROM sales GROUP BY StockCode, Description
            ORDER BY revenue DESC LIMIT 10
        """, conn)
        customers = pd.read_sql_query("""
            SELECT CustomerID, ROUND(SUM(Revenue), 2) AS revenue,
                   COUNT(DISTINCT InvoiceNo) AS orders
            FROM sales WHERE CustomerID IS NOT NULL
            GROUP BY CustomerID ORDER BY revenue DESC LIMIT 10
        """, conn)

    total_revenue = float(sales["Revenue"].sum())
    total_orders = int(sales["InvoiceNo"].nunique())
    identified_customers = int(sales["CustomerID"].nunique())
    kpis = {
        "completed_sales_lines": int(len(sales)),
        "revenue_gbp": round(total_revenue, 2),
        "unique_orders": total_orders,
        "identified_customers": identified_customers,
        "average_order_value_gbp": round(total_revenue / total_orders, 2) if total_orders else 0,
        "units_sold": int(sales["Quantity"].sum()),
    }
    pd.DataFrame([kpis]).to_csv(REPORT_DIR / "key_metrics.csv", index=False)
    monthly.to_csv(REPORT_DIR / "monthly_sales.csv", index=False)
    countries.to_csv(REPORT_DIR / "top_countries.csv", index=False)
    products.to_csv(REPORT_DIR / "top_products.csv", index=False)
    customers.to_csv(REPORT_DIR / "top_customers.csv", index=False)

    # Monthly revenue
    fig, ax = plt.subplots(figsize=(11, 5))
    sns.lineplot(data=monthly, x="InvoiceMonth", y="revenue", marker="o", ax=ax)
    ax.set(title="Monthly Revenue", xlabel="Invoice month", ylabel="Revenue (£)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "monthly_revenue.png", dpi=160)
    plt.close(fig)

    # Revenue by country
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=countries, y="Country", x="revenue", ax=ax)
    ax.set(title="Top 10 Countries by Revenue", xlabel="Revenue (£)", ylabel="Country")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "top_countries_revenue.png", dpi=160)
    plt.close(fig)

    # Top products
    plot_products = products.sort_values("revenue", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=plot_products, y="Description", x="revenue", ax=ax)
    ax.set(title="Top 10 Products by Revenue", xlabel="Revenue (£)", ylabel="Product")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "top_products_revenue.png", dpi=160)
    plt.close(fig)

    # Day-of-week sales pattern
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday = sales.groupby("DayOfWeek", as_index=False)["Revenue"].sum()
    weekday["DayOfWeek"] = pd.Categorical(weekday["DayOfWeek"], categories=weekday_order, ordered=True)
    weekday = weekday.sort_values("DayOfWeek")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=weekday, x="DayOfWeek", y="Revenue", ax=ax)
    ax.set(title="Revenue by Day of Week", xlabel="Day", ylabel="Revenue (£)")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "revenue_by_weekday.png", dpi=160)
    plt.close(fig)

    print("Key metrics:")
    for key, value in kpis.items():
        print(f"  {key}: {value}")
    print(f"Reports: {REPORT_DIR}")
    print(f"Charts: {FIG_DIR}")
    return kpis

if __name__ == "__main__":
    analyze()

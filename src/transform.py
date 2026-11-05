"""Clean Online Retail transactions using explicit, auditable business rules."""
import pandas as pd

REQUIRED_COLUMNS = [
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country",
]

def transform(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Return completed-sale lines and a quality summary.

    Unknown CustomerIDs remain in the sales fact table. They are excluded only
    from customer-level analysis. Cancellation invoices and invalid quantities
    or prices are excluded from completed-sales KPIs.
    """
    df = raw.copy()
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {missing_columns}")

    initial_rows = len(df)
    df = df[REQUIRED_COLUMNS].copy()
    exact_duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates()

    # Normalize text fields without changing identifier meaning.
    for col in ["InvoiceNo", "StockCode", "Description", "Country"]:
        df[col] = df[col].astype("string").str.strip()
    df["InvoiceNo"] = df["InvoiceNo"].str.upper()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce").astype("Int64")

    invalid_dates = int(df["InvoiceDate"].isna().sum())
    missing_descriptions = int(df["Description"].isna().sum())
    missing_customers = int(df["CustomerID"].isna().sum())
    cancellation_mask = df["InvoiceNo"].str.startswith("C", na=False)
    cancellations = int(cancellation_mask.sum())
    invalid_quantity = int((df["Quantity"].isna() | (df["Quantity"] <= 0)).sum())
    invalid_price = int((df["UnitPrice"].isna() | (df["UnitPrice"] <= 0)).sum())

    # Sales fact table: positive quantity/price, valid timestamp, non-cancelled invoice.
    valid = (
        ~cancellation_mask
        & df["InvoiceDate"].notna()
        & df["Quantity"].gt(0)
        & df["UnitPrice"].gt(0)
    )
    sales = df.loc[valid].copy()
    sales["Description"] = sales["Description"].fillna("Unknown product")
    sales["Country"] = sales["Country"].fillna("Unknown")
    sales["Revenue"] = sales["Quantity"] * sales["UnitPrice"]
    sales["InvoiceMonth"] = sales["InvoiceDate"].dt.to_period("M").astype(str)
    sales["InvoiceYear"] = sales["InvoiceDate"].dt.year
    sales["DayOfWeek"] = sales["InvoiceDate"].dt.day_name()

    quality = {
        "source_rows": initial_rows,
        "exact_duplicate_rows_removed": exact_duplicates,
        "rows_after_deduplication": len(df),
        "missing_customer_id_rows": missing_customers,
        "missing_description_rows": missing_descriptions,
        "invalid_invoice_date_rows": invalid_dates,
        "cancellation_rows": cancellations,
        "non_positive_or_missing_quantity_rows": invalid_quantity,
        "non_positive_or_missing_unit_price_rows": invalid_price,
        "completed_sales_rows": len(sales),
        "completed_sales_rows_removed_by_business_rules": len(df) - len(sales),
        "sales_rows_without_customer_id": int(sales["CustomerID"].isna().sum()),
    }
    return sales, quality

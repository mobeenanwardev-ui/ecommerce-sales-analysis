"""Load transformed sales data into reproducible analytical destinations."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_DIR = ROOT / "outputs" / "reports"
DB_PATH = ROOT / "outputs" / "ecommerce_sales.db"

def load(sales: pd.DataFrame, quality: dict) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    sales.to_csv(PROCESSED_DIR / "cleaned_sales.csv", index=False)
    pd.DataFrame([quality]).to_csv(OUTPUT_DIR / "data_quality_summary.csv", index=False)

    db_frame = sales.copy()
    db_frame["CustomerID"] = db_frame["CustomerID"].astype("Int64").astype("string")
    with sqlite3.connect(DB_PATH) as connection:
        db_frame.to_sql("sales", connection, if_exists="replace", index=False)
        pd.DataFrame([quality]).to_sql(
            "data_quality_summary", connection, if_exists="replace", index=False
        )
    print(f"Loaded {len(sales):,} sales lines into {DB_PATH}")

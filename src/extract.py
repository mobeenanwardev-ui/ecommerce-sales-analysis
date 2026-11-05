"""Download and save the original UCI Online Retail dataset."""
from pathlib import Path
import pandas as pd
from ucimlrepo import fetch_ucirepo

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
RAW_FILE = RAW_DIR / "online_retail.xlsx"

def extract() -> pd.DataFrame:
    """Fetch dataset 352 from UCI, persist the source workbook, return features."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    dataset = fetch_ucirepo(id=352)
    frame = dataset.data.features.copy()
    # ucimlrepo returns the feature table; persist a reproducible local snapshot.
    # Excel is used to retain the source dataset's familiar tabular format.
    frame.to_excel(RAW_FILE, index=False)
    print(f"Extracted {len(frame):,} rows and {len(frame.columns)} columns.")
    print(f"Raw snapshot: {RAW_FILE}")
    return frame

if __name__ == "__main__":
    extract()

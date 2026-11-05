"""Run extraction, transformation, loading, and analysis in sequence."""
from src.extract import extract
from src.transform import transform
from src.load import load
from src.analyze import analyze

def main() -> None:
    raw = extract()
    sales, quality = transform(raw)
    print("Data quality summary:")
    for key, value in quality.items():
        print(f"  {key}: {value}")
    load(sales, quality)
    analyze()
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()

"""Week 3 Client Project: Dataset Cleaning and Aggregation with Pandas."""

from pathlib import Path
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"


def create_sample_dataset(csv_path: Path) -> None:
    """Create a realistic messy retail sales CSV if not already present."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    raw_df = pd.DataFrame(
        {
            "OrderID": [1001, 1002, 1003, 1003, 1004, 1005, 1006, 1007, 1008],
            "Region": ["North", "South", "East", "East", "West", "North", None, "South", "West"],
            "Category": ["Electronics", "Furniture", "Electronics", "Electronics", "Office", "Furniture", "Office", "Electronics", "Furniture"],
            "Units": [2, 1, 3, 3, np.nan, 4, 2, 1, 5],
            "UnitPrice": [450.0, 300.0, 450.0, 450.0, 45.0, 300.0, 45.0, np.nan, 300.0],
        }
    )
    raw_df.to_csv(csv_path, index=False)


def clean_and_aggregate(csv_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load raw sales CSV, remove duplicates/missing values, and aggregate by Region & Category."""
    df = pd.read_csv(csv_path)
    initial_rows = len(df)

    # Remove exact duplicate orders
    df = df.drop_duplicates(subset=["OrderID"]).copy()

    # Drop rows where Region is missing, impute numeric missing values with median
    df = df.dropna(subset=["Region"]).copy()
    df["Units"] = df["Units"].fillna(df["Units"].median())
    df["UnitPrice"] = df["UnitPrice"].fillna(df["UnitPrice"].median())

    df["Revenue"] = df["Units"] * df["UnitPrice"]

    summary = (
        df.groupby(["Region", "Category"], as_index=False)
        .agg(
            Orders=("OrderID", "count"),
            Avg_Units=("Units", "mean"),
            Avg_Revenue=("Revenue", "mean"),
            Total_Revenue=("Revenue", "sum"),
        )
        .sort_values("Total_Revenue", ascending=False)
    )

    print(f"Initial rows: {initial_rows} | Cleaned rows: {len(df)}")
    return df, summary


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_csv = DATA_DIR / "raw_sales.csv"
    if not raw_csv.exists():
        create_sample_dataset(raw_csv)

    cleaned_df, summary_df = clean_and_aggregate(raw_csv)
    cleaned_df.to_csv(OUTPUT_DIR / "cleaned_sales.csv", index=False)
    summary_df.to_csv(OUTPUT_DIR / "sales_aggregation_summary.csv", index=False)

    print("\n=== Aggregated Sales Summary ===")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()

"""Week 3 Hands-On: NumPy Arrays, Broadcasting, and Pandas Series/DataFrames."""

import numpy as np
import pandas as pd


def demonstrate_numpy() -> None:
    """Demonstrate NumPy array creation, vectorized ops, and broadcasting."""
    print("=== NumPy Operations & Broadcasting ===")
    arr = np.array([[10, 20, 30], [40, 50, 60]], dtype=float)
    weights = np.array([0.2, 0.3, 0.5])  # shape (3,) broadcasts across rows

    weighted = arr * weights
    normalized = (arr - arr.mean(axis=0)) / arr.std(axis=0)

    print("Original array:\n", arr)
    print("Broadcasted weighted array:\n", weighted)
    print("Row sums:", weighted.sum(axis=1))
    print("Column-wise standardized:\n", np.round(normalized, 3))


def demonstrate_pandas() -> None:
    """Demonstrate Pandas Series, DataFrame indexing, and groupby."""
    print("\n=== Pandas Series, DataFrame, Indexing & Grouping ===")
    temps = pd.Series([22.1, 24.5, 19.8, 27.0], index=["Mon", "Tue", "Wed", "Thu"], name="Temp_C")
    print("Series:\n", temps)

    df = pd.DataFrame(
        {
            "Employee": ["Alice", "Bob", "Charlie", "Diana", "Evan"],
            "Department": ["Data", "Engineering", "Data", "Engineering", "Data"],
            "Salary": [95000, 105000, 88000, 112000, 92000],
            "Projects": [5, 7, 4, 8, 6],
        }
    )
    print("\nDataFrame (.loc filter for Data dept):\n", df.loc[df["Department"] == "Data"])
    grouped = df.groupby("Department", as_index=False).agg(
        Avg_Salary=("Salary", "mean"),
        Total_Projects=("Projects", "sum"),
        Headcount=("Employee", "count"),
    )
    print("\nGrouped Summary:\n", grouped)


if __name__ == "__main__":
    demonstrate_numpy()
    demonstrate_pandas()

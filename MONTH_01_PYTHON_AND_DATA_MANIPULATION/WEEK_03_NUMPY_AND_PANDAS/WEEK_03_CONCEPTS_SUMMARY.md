# Week 3 Concepts Summary: NumPy and Pandas for Data Manipulation

## Topics Covered
1. **NumPy Arrays & Vectorization**: Creating `ndarray` objects, element-wise operations, and axis aggregations (`mean`, `std`, `sum`).
2. **Broadcasting**: Applying 1D weight/scaling vectors across 2D matrices without explicit Python loops.
3. **Pandas Series & DataFrames**: Labeled 1D/2D structures, `.loc` boolean indexing, and column creation.
4. **Data Cleaning & Grouping**: Deduplication (`drop_duplicates`), missing-value handling (`dropna`, `fillna`), and `groupby().agg()`.

## Deliverables Implemented
- `numpy_pandas_practice.py`: Demonstrates NumPy broadcasting, standardization, Pandas Series, `.loc` filtering, and groupby aggregations.
- `dataset_cleaning_aggregation_client_project.py`: Generates `data/raw_sales.csv`, cleans duplicates and missing values, computes revenue, and exports `outputs/cleaned_sales.csv` and `outputs/sales_aggregation_summary.csv`.

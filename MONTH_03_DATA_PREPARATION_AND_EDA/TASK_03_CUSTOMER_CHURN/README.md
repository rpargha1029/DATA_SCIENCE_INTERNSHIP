# Task 3: Customer Churn Data Preparation & EDA

## Objective
Prepare telecom customer data for modeling using data cleaning, feature engineering, encoding, and exploratory data analysis.

## Tasks Implemented
- **Data Understanding**: Inspect `.info()`, `.describe()`, and detect blank strings (`" "`) in `TotalCharges`.
- **Data Cleaning**: Convert `TotalCharges` from `object` to `float`, handle missing values, and flag/remove invalid rows.
- **Feature Engineering**:
  - `TenureGroup`: Bucketed tenure (`0-12`, `13-24`, `25-48`, `49-60`, `61+` months).
  - `AvgMonthlySpend`: `TotalCharges / tenure` (safely handling `tenure == 0`).
  - Binary `Yes`/`No` encoding to `1`/`0`.
  - One-hot encoding for categorical columns (`Contract`, `InternetService`, etc.).
- **EDA & Visualization**: Churn countplot, Contract vs. Churn barplot, Correlation heatmap, MonthlyCharges by Churn boxplot, and Pairplot.
- **Deliverables**: Jupyter notebook (`notebooks/customer_churn_eda.ipynb`), Python pipeline (`src/churn_pipeline.py`), cleaned CSV (`outputs/cleaned_telco_churn.csv`), and Top 5 insights (`outputs/TOP_5_INSIGHTS.md`).

## Dataset Source & Manual Download
- **Dataset**: Telco Customer Churn (Kaggle, ~7,043 rows)
- **URL**: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- **Setup**: Download `WA_Fn-UseC_-Telco-Customer-Churn.csv` and place it in `TASK_03_CUSTOMER_CHURN/data/`.

## Execution
```bash
python src/churn_pipeline.py
```

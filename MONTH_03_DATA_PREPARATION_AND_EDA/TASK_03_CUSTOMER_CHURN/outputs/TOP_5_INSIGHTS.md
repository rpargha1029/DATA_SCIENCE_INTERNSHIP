# Task 3: Customer Churn — Top 5 Insights Summary

> **Note**: Place `WA_Fn-UseC_-Telco-Customer-Churn.csv` in `data/` and run `python src/churn_pipeline.py` to generate `outputs/cleaned_telco_churn.csv` and all 5 EDA charts.

1. **Contract Length Strongly Drives Retention**: Customers on month-to-month contracts exhibit substantially higher churn rates than those on one-year or two-year contracts.
2. **Early-Tenure Vulnerability**: The `0-12 months` `TenureGroup` accounts for the highest concentration of churned customers; retention stabilizes significantly after 24 months.
3. **Higher Monthly Charges Correlate with Churn**: Churned customers tend to have a higher median `MonthlyCharges` than retained customers, indicating price sensitivity on premium tiers.
4. **TotalCharges Data Type & Blank Strings**: Raw `TotalCharges` arrives as `object` due to whitespace `" "` entries for `tenure == 0` customers, requiring explicit `pd.to_numeric(..., errors="coerce")` cleaning.
5. **Derived Spend Feature (`AvgMonthlySpend`)**: Comparing `AvgMonthlySpend` (`TotalCharges / tenure`) against current `MonthlyCharges` highlights customers experiencing recent bill increases.

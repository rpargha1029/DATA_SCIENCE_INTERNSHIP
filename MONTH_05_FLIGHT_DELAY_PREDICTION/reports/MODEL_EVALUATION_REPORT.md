# Month 5 Report: Flight Delay Prediction Using Machine Learning

## 1. Target Definition & Leakage Prevention
- **Target Variable**: Binary delay indicator (`ArrDel15` or `Delay`, or `ArrDelay > 15` minutes when `ArrDel15` is absent).
- **Leakage Controls**: Post-departure/arrival columns (`ArrDelay`, `DepDelay`, `TaxiIn`, `TaxiOut`, `AirTime`, `CarrierDelay`, `WeatherDelay`, etc.) are explicitly excluded prior to training so predictions rely only on pre-flight schedule, carrier (`Airline`), and route (`Origin`, `Dest`, `FlightWeekday`, `FlightMonth`) features.

## 2. Modeling Pipeline
1. Drop columns with > 40% missing values.
2. Extract `FlightWeekday` and `FlightMonth` from `FlightDate`.
3. Encode `Airline`, `Origin`, and `Dest` via `OneHotEncoder(handle_unknown="ignore", max_categories=50)` and scale numeric features inside a `ColumnTransformer`.
4. Train **Logistic Regression** and **Random Forest** on a stratified 80/20 split.

## 3. Model Evaluation
> **Status**: Pending local dataset in `MONTH_05_FLIGHT_DELAY_PREDICTION/data/`. Run `python src/train_flight_delay.py` after placing the Kaggle Airline Delay CSV in `data/` to populate actual metrics in `reports/metrics.json` and generate the Confusion Matrix and ROC Curve plots in `outputs/`.

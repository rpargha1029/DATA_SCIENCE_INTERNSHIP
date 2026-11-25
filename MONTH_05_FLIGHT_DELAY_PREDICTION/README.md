# Month 5: Flight Delay Prediction Using Machine Learning

## Objective
Train and evaluate binary classification models (Logistic Regression and Random Forest) to predict whether a flight will be delayed or on time using airline, route, and schedule features while preventing data leakage.

## Tasks Implemented
- **Data Preparation**:
  - Drop columns exceeding a missing-value threshold (default: > 40% missing).
  - Extract `FlightWeekday` (0–6) and `FlightMonth` (1–12) from `FlightDate`.
  - Encode `Airline`, `Origin`, and `Dest` inside a Scikit-learn `ColumnTransformer` (`OneHotEncoder(handle_unknown="ignore")`).
  - **Target Definition & Leakage Prevention**: Uses `ArrDel15` (or `Delay` / `IsDelayed`, or `ArrDelay > 15`) as the binary target and explicitly excludes post-departure/arrival leakage columns (`ArrDelay`, `DepDelay`, `TaxiOut`, `TaxiIn`, `AirTime`, `CarrierDelay`, `WeatherDelay`, etc.).
- **Model Building & Evaluation**:
  - Stratified 80/20 Train/Test split.
  - Train **Logistic Regression** and **Random Forest** classifiers.
  - Evaluate Accuracy, Precision, Recall, F1-Score, ROC-AUC, Confusion Matrix, and Classification Report.
  - Save Confusion Matrix and ROC Curve plots to `outputs/` and the best `.pkl` pipeline to `models/flight_delay_best_model.pkl`.

## Dataset Source & Manual Download
- **Dataset**: Airline Delay Dataset (Kaggle)
- **URL**: https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022 (or compatible Kaggle Airline Delay CSV with `FlightDate`, `Airline`, `Origin`, `Dest`, and delay target).
- **Setup**: Place the downloaded CSV (e.g., `flight_delay.csv`) inside `MONTH_05_FLIGHT_DELAY_PREDICTION/data/`.

## Execution
```bash
python src/train_flight_delay.py
```

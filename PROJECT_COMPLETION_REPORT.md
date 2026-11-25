# Five-Month Data Science Internship — Project Completion & Audit Report

## 1. Month-Wise & Assignment-Wise Status

| Month / Task | Status | Notes |
| :--- | :--- | :--- |
| **Month 1 — Week 1: Python Basics** | `COMPLETED AND TESTED` | All 3 scripts (`temperature_converter.py`, `calculator.py`, `average_temperature_client_project.py`) executed and verified. |
| **Month 1 — Week 2: Data Structures & Functions** | `COMPLETED AND TESTED` | `data_structures_and_transformations.py` and `data_cleaning_client_project.py` executed and verified. |
| **Month 1 — Week 3: NumPy & Pandas** | `COMPLETED AND TESTED` | `numpy_pandas_practice.py` and `dataset_cleaning_aggregation_client_project.py` executed; CSV outputs generated. |
| **Month 1 — Week 4: Data Visualization** | `COMPLETED AND TESTED` | `visualization_dashboard.py` executed; 5 PNG plots generated in `outputs/`. |
| **Month 2 — Titanic Predictive Model** | `PENDING DATASET` | Code, 12-section notebook, and report implemented; pipeline logic verified on in-memory test fixture. Requires manual Kaggle download of `Titanic-Dataset.csv`. |
| **Month 3 — Task 3: Customer Churn EDA** | `PENDING DATASET` | Pipeline, 12-section notebook, and insights template implemented; logic verified on in-memory test fixture. Requires Kaggle `WA_Fn-UseC_-Telco-Customer-Churn.csv`. |
| **Month 3 — Task 4: Netflix Titles EDA** | `PENDING DATASET` | Pipeline (including 2-year trend forecast), 12-section notebook, and insights summary implemented; logic verified on in-memory test fixture. Requires Kaggle `netflix_titles.csv`. |
| **Month 3 — Bonus: 5-Slide Comparison Deck** | `COMPLETED AND TESTED` | `generate_comparison_deck.py` executed; `Business_vs_Entertainment_Comparison_Deck.pptx` (5 slides) generated and verified. |
| **Month 4 — Movie Recommendation System** | `PENDING DATASET` | Recommender (`src/recommender.py`), 12-section notebook, and optional Streamlit app (`app/streamlit_app.py`) implemented; TF-IDF + cosine similarity + `recommend()` verified on in-memory test fixture. Requires Kaggle TMDB 5000 CSVs. |
| **Month 5 — Flight Delay Prediction** | `PENDING DATASET` | Leakage-free classification pipeline (`src/train_flight_delay.py`), 12-section notebook, and report implemented; Logistic Regression & Random Forest verified on in-memory test fixture. Requires Kaggle Airline Delay CSV. |

---

## 2. Files Generated

- **Root**: `README.md`, `requirements.txt`, `.gitignore`, `PROJECT_COMPLETION_REPORT.md`
- **Month 1 (`MONTH_01_PYTHON_AND_DATA_MANIPULATION/`)**:
  - `README.md`
  - `WEEK_01_PYTHON_BASICS/`: `temperature_converter.py`, `calculator.py`, `average_temperature_client_project.py`, `WEEK_01_CONCEPTS_SUMMARY.md`
  - `WEEK_02_DATA_STRUCTURES_AND_FUNCTIONS/`: `data_structures_and_transformations.py`, `data_cleaning_client_project.py`, `WEEK_02_CONCEPTS_SUMMARY.md`
  - `WEEK_03_NUMPY_AND_PANDAS/`: `numpy_pandas_practice.py`, `dataset_cleaning_aggregation_client_project.py`, `data/raw_sales.csv`, `outputs/cleaned_sales.csv`, `outputs/sales_aggregation_summary.csv`, `WEEK_03_CONCEPTS_SUMMARY.md`
  - `WEEK_04_DATA_VISUALIZATION/`: `visualization_dashboard.py`, `data/employee_performance.csv`, 5 PNG plots in `outputs/`, `WEEK_04_CONCEPTS_SUMMARY.md`
- **Month 2 (`MONTH_02_TITANIC_PREDICTION/`)**:
  - `README.md`, `src/train_evaluate.py`, `notebooks/titanic_survival_prediction.ipynb`, `reports/MODEL_EVALUATION_REPORT.md`
- **Month 3 (`MONTH_03_DATA_PREPARATION_AND_EDA/`)**:
  - `README.md`, `generate_comparison_deck.py`, `Business_vs_Entertainment_Comparison_Deck.pptx`
  - `TASK_03_CUSTOMER_CHURN/`: `README.md`, `src/churn_pipeline.py`, `notebooks/customer_churn_eda.ipynb`, `outputs/TOP_5_INSIGHTS.md`
  - `TASK_04_NETFLIX_EDA/`: `README.md`, `src/netflix_eda.py`, `notebooks/netflix_eda.ipynb`, `outputs/INSIGHTS_SUMMARY.md`
- **Month 4 (`MONTH_04_MOVIE_RECOMMENDATION_SYSTEM/`)**:
  - `README.md`, `src/recommender.py`, `notebooks/movie_recommender.ipynb`, `app/streamlit_app.py`
- **Month 5 (`MONTH_05_FLIGHT_DELAY_PREDICTION/`)**:
  - `README.md`, `src/train_flight_delay.py`, `notebooks/flight_delay_prediction.ipynb`, `reports/MODEL_EVALUATION_REPORT.md`

---

## 3. Verification & Test Results

- **Month 1 Scripts**: All 8 Python scripts executed end-to-end with exit code `0`, generating `cleaned_sales.csv`, `sales_aggregation_summary.csv`, and all 5 visualization PNGs.
- **Month 3 Bonus PPTX**: `generate_comparison_deck.py` executed with exit code `0`, producing a 5-slide `.pptx` file.
- **Notebooks**: All 5 `.ipynb` files validated against `nbformat` v4.
- **Months 2–5 Pipelines**: All core functions (`train_and_evaluate`, `clean_and_engineer_features`, `clean_and_engineer`, `prepare_movie_tags`, `build_and_save_model`, `recommend`, `prepare_flight_data`) verified against in-memory test DataFrames. Real Kaggle evaluation metrics are **not** fabricated and remain pending local dataset placement.

---

## 4. Pending Manual Actions (Kaggle Datasets)

1. **Month 2**: Download `Titanic-Dataset.csv` from https://www.kaggle.com/datasets/yasserh/titanic-dataset -> place in `MONTH_02_TITANIC_PREDICTION/data/`.
2. **Month 3 (Task 3)**: Download `WA_Fn-UseC_-Telco-Customer-Churn.csv` from https://www.kaggle.com/datasets/blastchar/telco-customer-churn -> place in `MONTH_03_DATA_PREPARATION_AND_EDA/TASK_03_CUSTOMER_CHURN/data/`.
3. **Month 3 (Task 4)**: Download `netflix_titles.csv` from https://www.kaggle.com/datasets/shivamb/netflix-shows -> place in `MONTH_03_DATA_PREPARATION_AND_EDA/TASK_04_NETFLIX_EDA/data/`.
4. **Month 4**: Download `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` from https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata -> place in `MONTH_04_MOVIE_RECOMMENDATION_SYSTEM/data/`.
5. **Month 5**: Download the Airline Delay CSV from https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022 -> place in `MONTH_05_FLIGHT_DELAY_PREDICTION/data/`.

---

## 5. Commands to Execute Every Project

```bash
# Month 1
python MONTH_01_PYTHON_AND_DATA_MANIPULATION/WEEK_01_PYTHON_BASICS/temperature_converter.py --demo
python MONTH_01_PYTHON_AND_DATA_MANIPULATION/WEEK_01_PYTHON_BASICS/calculator.py --demo
python MONTH_01_PYTHON_AND_DATA_MANIPULATION/WEEK_01_PYTHON_BASICS/average_temperature_client_project.py
python MONTH_01_PYTHON_AND_DATA_MANIPULATION/WEEK_02_DATA_STRUCTURES_AND_FUNCTIONS/data_structures_and_transformations.py
python MONTH_01_PYTHON_AND_DATA_MANIPULATION/WEEK_02_DATA_STRUCTURES_AND_FUNCTIONS/data_cleaning_client_project.py
python MONTH_01_PYTHON_AND_DATA_MANIPULATION/WEEK_03_NUMPY_AND_PANDAS/numpy_pandas_practice.py
python MONTH_01_PYTHON_AND_DATA_MANIPULATION/WEEK_03_NUMPY_AND_PANDAS/dataset_cleaning_aggregation_client_project.py
python MONTH_01_PYTHON_AND_DATA_MANIPULATION/WEEK_04_DATA_VISUALIZATION/visualization_dashboard.py

# Month 2 (after placing Titanic-Dataset.csv in data/)
python MONTH_02_TITANIC_PREDICTION/src/train_evaluate.py

# Month 3 (after placing CSVs in respective data/ folders)
python MONTH_03_DATA_PREPARATION_AND_EDA/TASK_03_CUSTOMER_CHURN/src/churn_pipeline.py
python MONTH_03_DATA_PREPARATION_AND_EDA/TASK_04_NETFLIX_EDA/src/netflix_eda.py
python MONTH_03_DATA_PREPARATION_AND_EDA/generate_comparison_deck.py

# Month 4 (after placing TMDB 5000 CSVs in data/)
python MONTH_04_MOVIE_RECOMMENDATION_SYSTEM/src/recommender.py
streamlit run MONTH_04_MOVIE_RECOMMENDATION_SYSTEM/app/streamlit_app.py

# Month 5 (after placing Airline Delay CSV in data/)
python MONTH_05_FLIGHT_DELAY_PREDICTION/src/train_flight_delay.py
```

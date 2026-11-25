# GitHub & Classroom Submission Checklist (Months 1–6)

Use this checklist before uploading each month's project to GitHub and submitting on Google Classroom by the **20th of the respective month**.

---

## Global Pre-Upload Security & Repository Hygiene
- [ ] Verify `.gitignore` is at the repository root and excludes `.env`, `kaggle.json`, API keys, raw Kaggle CSVs, and large `.pkl` files (`> 50 MB`).
- [ ] Confirm no hardcoded API keys (e.g., `TMDB_API_KEY`) or personal credentials appear in any `.py`, `.ipynb`, or `.md` file.
- [ ] Confirm `requirements.txt` and root `README.md` are up to date.
- [ ] *(Optional for large `.pkl` files)* Initialize Git LFS if you explicitly choose to track model binaries: `git lfs track "*.pkl"`.

---

## Month-Wise Checklists

### Month 1 — Python Basics and Data Manipulation
- [x] `MONTH_01_PYTHON_AND_DATA_MANIPULATION/README.md` exists with clear instructions.
- [x] Weeks 1–4 scripts (`temperature_converter.py`, `calculator.py`, `average_temperature_client_project.py`, `data_structures_and_transformations.py`, `data_cleaning_client_project.py`, `numpy_pandas_practice.py`, `dataset_cleaning_aggregation_client_project.py`, `visualization_dashboard.py`) run cleanly.
- [x] Concept summaries (`WEEK_01_CONCEPTS_SUMMARY.md` to `WEEK_04_CONCEPTS_SUMMARY.md`) and Week 4 PNG plots are present.
- [ ] Push to GitHub and submit Month 1 link/files on Google Classroom by the **20th of Month 1**.

### Month 2 — Titanic Predictive Model
- [x] `MONTH_02_TITANIC_PREDICTION/README.md`, `src/train_evaluate.py`, `notebooks/titanic_survival_prediction.ipynb`, and `reports/MODEL_EVALUATION_REPORT.md` are present.
- [ ] Place `Titanic-Dataset.csv` in `data/` locally and run `python src/train_evaluate.py` + execute notebook top-to-bottom.
- [ ] Verify `data/Titanic-Dataset.csv` is **not** committed if keeping repository lightweight (source link is documented in `README.md`).
- [ ] Push to GitHub and submit on Google Classroom by the **20th of Month 2**.

### Month 3 — Customer Churn & Netflix EDA
- [x] `TASK_03_CUSTOMER_CHURN/` and `TASK_04_NETFLIX_EDA/` each have `README.md`, `src/`, `notebooks/`, and `outputs/`.
- [x] Bonus 5-slide comparison deck (`Business_vs_Entertainment_Comparison_Deck.pptx`) is generated.
- [ ] Place `WA_Fn-UseC_-Telco-Customer-Churn.csv` and `netflix_titles.csv` in their respective `data/` folders locally and run both pipelines + notebooks.
- [ ] Include generated EDA PNGs and insight summaries (`TOP_5_INSIGHTS.md`, `INSIGHTS_SUMMARY.md`) in submission.
- [ ] Push to GitHub and submit on Google Classroom by the **20th of Month 3**.

### Month 4 — Content-Based Movie Recommendation System
- [x] `MONTH_04_MOVIE_RECOMMENDATION_SYSTEM/README.md`, `src/recommender.py`, `notebooks/movie_recommender.ipynb`, and `app/streamlit_app.py` are present.
- [ ] Place `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` in `data/` locally and run `python src/recommender.py`.
- [ ] Launch `streamlit run app/streamlit_app.py` and capture UI screenshot(s) in `outputs/`.
- [ ] Confirm `similarity_matrix.pkl` (large matrix) and raw CSVs are excluded by `.gitignore` (or tracked via Git LFS).
- [ ] Push to GitHub and submit on Google Classroom by the **20th of Month 4**.

### Month 5 — Flight Delay Prediction Using Machine Learning
- [x] `MONTH_05_FLIGHT_DELAY_PREDICTION/README.md`, `src/train_flight_delay.py`, `notebooks/flight_delay_prediction.ipynb`, and `reports/MODEL_EVALUATION_REPORT.md` are present.
- [ ] Place Airline Delay CSV in `data/` locally and run `python src/train_flight_delay.py` + execute notebook.
- [ ] Verify Confusion Matrix, ROC Curve PNGs, and `MODEL_EVALUATION_REPORT.md` are updated with actual metrics.
- [ ] Confirm large Airline Delay CSVs and `.pkl` files are excluded by `.gitignore` (or tracked via Git LFS).
- [ ] Push to GitHub and submit on Google Classroom by the **20th of Month 5**.

### Month 6 — Pending Official Assignment PDF
- [x] `MONTH_06/README.md` placeholder created (no invented tasks).
- [ ] Obtain official Month 6 PDF, implement tasks, test, and submit by the **20th of Month 6**.

---

## Exact Git Commands (Run Only When Ready to Upload)

> **Note**: Nothing has been pushed automatically. Run these commands manually from `e:\DATA_SCIENCE_INTERNSHIP` when you are ready:

```bash
# 1. Initialize repository (if not already initialized)
cd e:\DATA_SCIENCE_INTERNSHIP
git init

# 2. Verify ignored files (confirm no CSVs, .env, or large .pkl files are staged)
git status

# 3. Stage and commit
git add .
git commit -m "Initialize Skybrisk Data Science Internship portfolio (Months 1-5 + Month 6 placeholder)"

# 4. Connect to your GitHub remote and push
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
git push -u origin main
```

# Month 2: Titanic Survival Predictive Model

## Objective
Build and evaluate Scikit-learn predictive models to predict passenger survival (`Survived`) on the Titanic dataset.

## Tasks Implemented
- Load and explore the Titanic dataset (`shape`, `info`, missing values, summary statistics).
- Preprocess data: handle missing values (`Age` median imputation, `Embarked` mode imputation, drop high-missing `Cabin` and identifier columns `PassengerId`, `Name`, `Ticket`) and encode categorical features (`Sex`, `Embarked`).
- Split data into 80% training and 20% testing sets with stratification.
- Train three Scikit-learn models: **Logistic Regression**, **Decision Tree**, and **Random Forest**.
- Evaluate models using **Accuracy**, **Precision**, **Recall**, **F1-Score**, **Mean Squared Error (MSE)**, and **R² Score** (as specified in the assignment PDF), plus confusion matrices.
- Persist the best-performing model to `models/titanic_best_model.pkl` and generate a short report in `reports/`.

## Technologies
- Python, NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, Joblib, Jupyter Notebook

## Dataset Source & Manual Download
- **Dataset**: Titanic Dataset (Kaggle)
- **URL**: https://www.kaggle.com/datasets/yasserh/titanic-dataset
- **Setup**:
  1. Download `Titanic-Dataset.csv` from the Kaggle link above (or via `kaggle datasets download -d yasserh/titanic-dataset`).
  2. Place `Titanic-Dataset.csv` inside `MONTH_02_TITANIC_PREDICTION/data/`.

## Execution Instructions
```bash
# Train and evaluate models (requires data/Titanic-Dataset.csv)
python src/train_evaluate.py

# Or run the Jupyter notebook
jupyter nbconvert --to notebook --execute notebooks/titanic_survival_prediction.ipynb --inplace
```

## Results & Learning Outcomes
- End-to-end Scikit-learn `Pipeline` + `ColumnTransformer` prevents train/test data leakage during imputation and encoding.
- Compares linear (Logistic Regression) vs. tree-based (Decision Tree, Random Forest) classifiers on tabular data.
- Actual metrics are populated in `reports/MODEL_EVALUATION_REPORT.md` upon running with the downloaded Kaggle CSV.

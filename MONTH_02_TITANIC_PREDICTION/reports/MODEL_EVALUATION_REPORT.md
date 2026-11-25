# Month 2 Report: Titanic Survival Prediction

## 1. Approach and Steps Followed
1. **Data Loading & Exploration**: Load `Titanic-Dataset.csv` and inspect feature distributions, data types, and missingness (`Age`, `Cabin`, `Embarked`).
2. **Preprocessing**:
   - Numeric features (`Pclass`, `Age`, `SibSp`, `Parch`, `Fare`): Median imputation + `StandardScaler`.
   - Categorical features (`Sex`, `Embarked`): Most-frequent imputation + `OneHotEncoder(handle_unknown="ignore")`.
   - Identifier/high-cardinality columns (`PassengerId`, `Name`, `Ticket`, `Cabin`) are excluded from the baseline feature set.
3. **Train/Test Split**: Stratified 80/20 split (`random_state=42`) to preserve survival class balance.
4. **Model Training**: Trained Logistic Regression, Decision Tree (`max_depth=5`), and Random Forest (`n_estimators=200`, `max_depth=7`) inside leak-free `Pipeline`s.
5. **Evaluation**: Evaluated Accuracy, Precision, Recall, F1-Score, Mean Squared Error (MSE), R² Score, and Confusion Matrix.

## 2. Model Performance
> **Status**: Pending local dataset (`data/Titanic-Dataset.csv`). Run `python src/train_evaluate.py` after placing the Kaggle CSV in `data/` to populate actual metrics in `reports/metrics.json`.

## 3. Observations and Conclusions
- Using `ColumnTransformer` inside a Scikit-learn `Pipeline` ensures imputation statistics (median/mode) and scaling parameters are learned strictly from `X_train`, preventing data leakage.
- Tree-based ensembles (Random Forest) typically capture non-linear interactions (e.g., `Sex` × `Pclass` × `Age`) better than linear Logistic Regression on Titanic tabular features.

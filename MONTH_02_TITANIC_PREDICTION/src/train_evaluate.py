"""Month 2: Titanic Survival Predictive Modeling Pipeline."""

from pathlib import Path
import json
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = BASE_DIR / "reports"

NUMERIC_FEATURES = ["Pclass", "Age", "SibSp", "Parch", "Fare"]
CATEGORICAL_FEATURES = ["Sex", "Embarked"]
TARGET_COL = "Survived"


def locate_dataset() -> Path:
    """Locate the Kaggle Titanic CSV inside data/ or raise actionable instructions."""
    for candidate in ("Titanic-Dataset.csv", "titanic.csv", "train.csv"):
        path = DATA_DIR / candidate
        if path.exists():
            return path
    raise FileNotFoundError(
        f"Titanic dataset not found in {DATA_DIR}.\n"
        "Please download 'Titanic-Dataset.csv' from:\n"
        "  https://www.kaggle.com/datasets/yasserh/titanic-dataset\n"
        f"and place it in: {DATA_DIR / 'Titanic-Dataset.csv'}"
    )


def load_and_clean_data(csv_path: Path) -> pd.DataFrame:
    """Load Titanic CSV and retain modeling features + target."""
    df = pd.read_csv(csv_path)
    required = NUMERIC_FEATURES + CATEGORICAL_FEATURES + [TARGET_COL]
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing expected columns in dataset: {missing_cols}")
    return df[required].dropna(subset=[TARGET_COL]).copy()


def build_preprocessor() -> ColumnTransformer:
    """Create ColumnTransformer for numeric imputation/scaling and categorical encoding."""
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )


def train_and_evaluate(df: pd.DataFrame, save_artifacts: bool = True) -> dict:
    """Split data, train 3 models, evaluate metrics, and optionally save artifacts."""
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET_COL].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=7, random_state=42),
    }

    results = {}
    best_name = None
    best_acc = -1.0
    best_pipeline = None

    for name, estimator in models.items():
        pipe = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor()),
                ("classifier", estimator),
            ]
        )
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)

        metrics = {
            "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
            "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
            "mse": round(float(mean_squared_error(y_test, y_pred)), 4),
            "r2_score": round(float(r2_score(y_test, y_pred)), 4),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
            "classification_report": classification_report(y_test, y_pred, zero_division=0),
        }
        results[name] = metrics

        if metrics["accuracy"] > best_acc:
            best_acc = metrics["accuracy"]
            best_name = name
            best_pipeline = pipe

    if save_artifacts and best_pipeline is not None:
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        joblib.dump(best_pipeline, MODELS_DIR / "titanic_best_model.pkl")

        # Save confusion matrix plot for best model
        cm = np.array(results[best_name]["confusion_matrix"])
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_title(f"Titanic Confusion Matrix ({best_name})")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        fig.tight_layout()
        fig.savefig(OUTPUTS_DIR / "titanic_confusion_matrix.png", dpi=150)
        plt.close(fig)

        # Save metrics JSON
        with open(REPORTS_DIR / "metrics.json", "w", encoding="utf-8") as f:
            json.dump({"best_model": best_name, "models": results}, f, indent=2)

    return {"best_model": best_name, "models": results}


def main() -> None:
    csv_path = locate_dataset()
    df = load_and_clean_data(csv_path)
    summary = train_and_evaluate(df, save_artifacts=True)
    print(f"Best Model: {summary['best_model']}")
    for name, m in summary["models"].items():
        print(
            f"{name:20s} | Acc: {m['accuracy']:.4f} | F1: {m['f1_score']:.4f} | "
            f"MSE: {m['mse']:.4f} | R2: {m['r2_score']:.4f}"
        )


if __name__ == "__main__":
    main()

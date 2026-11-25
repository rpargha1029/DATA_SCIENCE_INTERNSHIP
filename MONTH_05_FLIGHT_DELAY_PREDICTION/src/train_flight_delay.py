"""Month 5: Flight Delay Prediction Classification Pipeline."""

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
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = BASE_DIR / "reports"

LEAKAGE_COLUMNS = {
    "ArrDelay",
    "ArrDelayMinutes",
    "DepDelay",
    "DepDelayMinutes",
    "ActualElapsedTime",
    "AirTime",
    "TaxiIn",
    "TaxiOut",
    "WheelsOn",
    "WheelsOff",
    "CarrierDelay",
    "WeatherDelay",
    "NASDelay",
    "SecurityDelay",
    "LateAircraftDelay",
    "Cancelled",
    "Diverted",
    "ArrTime",
    "DepTime",
}


def locate_dataset() -> Path:
    """Locate any Airline Delay CSV inside data/."""
    csv_files = sorted(DATA_DIR.glob("*.csv"))
    if csv_files:
        return csv_files[0]
    raise FileNotFoundError(
        f"Airline Delay CSV not found in {DATA_DIR}.\n"
        "Download from Kaggle (e.g., https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022)\n"
        f"and place the CSV inside: {DATA_DIR}"
    )


def prepare_flight_data(
    df: pd.DataFrame, missing_threshold: float = 0.40
) -> tuple[pd.DataFrame, pd.Series, list[str], list[str]]:
    """
    Clean flight data, construct binary target without leakage, extract FlightDate features,
    and drop columns exceeding missing_threshold.
    """
    work = df.copy()

    # Determine binary delay target without inventing labels
    if "ArrDel15" in work.columns:
        work = work.dropna(subset=["ArrDel15"]).copy()
        y = work["ArrDel15"].astype(int)
        target_col = "ArrDel15"
    elif "Delay" in work.columns:
        work = work.dropna(subset=["Delay"]).copy()
        y = work["Delay"].astype(int)
        target_col = "Delay"
    elif "ArrDelay" in work.columns:
        work = work.dropna(subset=["ArrDelay"]).copy()
        y = (work["ArrDelay"] > 15).astype(int)
        target_col = "ArrDelay"
    else:
        raise ValueError(
            "Could not construct delay target: expected 'ArrDel15', 'Delay', or 'ArrDelay' column."
        )

    # Extract weekday & month from FlightDate if present
    if "FlightDate" in work.columns:
        flight_dt = pd.to_datetime(work["FlightDate"], errors="coerce")
        work["FlightWeekday"] = flight_dt.dt.weekday
        work["FlightMonth"] = flight_dt.dt.month

    # Drop target, raw date, and post-departure leakage columns
    drop_cols = {target_col, "FlightDate"} | (LEAKAGE_COLUMNS & set(work.columns))
    X = work.drop(columns=[c for c in drop_cols if c in work.columns]).copy()

    # Drop columns with too many missing values
    missing_ratios = X.isna().mean()
    high_missing_cols = missing_ratios[missing_ratios > missing_threshold].index.tolist()
    if high_missing_cols:
        X = X.drop(columns=high_missing_cols)

    # Identify categorical (including Airline, Origin, Dest) and numeric columns
    preferred_cats = [c for c in ("Airline", "Origin", "Dest") if c in X.columns]
    other_cats = X.select_dtypes(include=["object", "category"]).columns.tolist()
    cat_cols = list(dict.fromkeys(preferred_cats + other_cats))
    num_cols = [c for c in X.select_dtypes(include=[np.number]).columns if c not in cat_cols]

    if not cat_cols and not num_cols:
        raise ValueError("No usable feature columns remain after preprocessing.")

    return X[num_cols + cat_cols], y, num_cols, cat_cols


def build_preprocessor(num_cols: list[str], cat_cols: list[str]) -> ColumnTransformer:
    """Build leak-free ColumnTransformer for numeric and categorical flight features."""
    transformers = []
    if num_cols:
        transformers.append(
            (
                "num",
                Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]),
                num_cols,
            )
        )
    if cat_cols:
        transformers.append(
            (
                "cat",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore", max_categories=50)),
                    ]
                ),
                cat_cols,
            )
        )
    return ColumnTransformer(transformers=transformers)


def train_and_evaluate(
    X: pd.DataFrame, y: pd.Series, num_cols: list[str], cat_cols: list[str], save_artifacts: bool = True
) -> dict:
    """Train Logistic Regression & Random Forest, evaluate metrics, and save plots/model."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42, n_jobs=-1),
    }

    results = {}
    roc_curves = {}
    best_name = None
    best_auc = -1.0
    best_pipeline = None

    for name, clf in models.items():
        pipe = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor(num_cols, cat_cols)),
                ("classifier", clf),
            ]
        )
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        y_prob = pipe.predict_proba(X_test)[:, 1]

        auc_val = float(roc_auc_score(y_test, y_prob)) if len(np.unique(y_test)) > 1 else 0.0
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_curves[name] = (fpr, tpr, auc_val)

        results[name] = {
            "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
            "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
            "roc_auc": round(auc_val, 4),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
            "classification_report": classification_report(y_test, y_pred, zero_division=0),
        }

        if auc_val > best_auc:
            best_auc = auc_val
            best_name = name
            best_pipeline = pipe

    if save_artifacts and best_pipeline is not None:
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        joblib.dump(best_pipeline, MODELS_DIR / "flight_delay_best_model.pkl")

        # Confusion Matrix Plot for Best Model
        cm = np.array(results[best_name]["confusion_matrix"])
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_title(f"Flight Delay Confusion Matrix ({best_name})")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        fig.tight_layout()
        fig.savefig(OUTPUTS_DIR / "flight_delay_confusion_matrix.png", dpi=150)
        plt.close(fig)

        # ROC Curve Comparison Plot
        fig, ax = plt.subplots(figsize=(7, 5))
        for name, (fpr, tpr, auc_val) in roc_curves.items():
            ax.plot(fpr, tpr, label=f"{name} (AUC = {auc_val:.3f})")
        ax.plot([0, 1], [0, 1], "k--", label="Random Baseline")
        ax.set_title("ROC Curve Comparison: Flight Delay Prediction")
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.legend(loc="lower right")
        fig.tight_layout()
        fig.savefig(OUTPUTS_DIR / "flight_delay_roc_curve.png", dpi=150)
        plt.close(fig)

        with open(REPORTS_DIR / "metrics.json", "w", encoding="utf-8") as f:
            json.dump({"best_model": best_name, "models": results}, f, indent=2)

    return {"best_model": best_name, "models": results}


def main() -> None:
    csv_path = locate_dataset()
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    X, y, num_cols, cat_cols = prepare_flight_data(df)
    summary = train_and_evaluate(X, y, num_cols, cat_cols, save_artifacts=True)
    print(f"Best Model: {summary['best_model']}")
    for name, m in summary["models"].items():
        print(
            f"{name:20s} | Acc: {m['accuracy']:.4f} | Prec: {m['precision']:.4f} | "
            f"Rec: {m['recall']:.4f} | ROC-AUC: {m['roc_auc']:.4f}"
        )


if __name__ == "__main__":
    main()

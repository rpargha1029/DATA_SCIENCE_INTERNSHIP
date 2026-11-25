"""Task 3: Customer Churn Data Preparation, Feature Engineering & EDA Pipeline."""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"


def locate_dataset() -> Path:
    """Locate the Telco Customer Churn CSV inside data/."""
    for name in ("WA_Fn-UseC_-Telco-Customer-Churn.csv", "telco_churn.csv", "churn.csv"):
        candidate = DATA_DIR / name
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Telco Customer Churn CSV not found in {DATA_DIR}.\n"
        "Download from: https://www.kaggle.com/datasets/blastchar/telco-customer-churn\n"
        f"and save as: {DATA_DIR / 'WA_Fn-UseC_-Telco-Customer-Churn.csv'}"
    )


def clean_and_engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Clean TotalCharges, handle missing/invalid rows, engineer features, and encode."""
    cleaned = df.copy()

    # Replace whitespace-only strings with NaN and convert TotalCharges to float
    if "TotalCharges" in cleaned.columns:
        cleaned["TotalCharges"] = pd.to_numeric(
            cleaned["TotalCharges"].astype(str).str.strip().replace("", np.nan),
            errors="coerce",
        )
        # Impute missing TotalCharges where tenure == 0 with 0.0, otherwise median
        zero_tenure_mask = cleaned["TotalCharges"].isna() & (cleaned["tenure"] == 0)
        cleaned.loc[zero_tenure_mask, "TotalCharges"] = 0.0
        cleaned["TotalCharges"] = cleaned["TotalCharges"].fillna(cleaned["TotalCharges"].median())

    # Remove invalid negative charges or duplicate customerIDs if present
    if "customerID" in cleaned.columns:
        cleaned = cleaned.drop_duplicates(subset=["customerID"]).copy()
    cleaned = cleaned[cleaned["MonthlyCharges"] >= 0].copy()

    # Feature Engineering: TenureGroup
    bins = [-1, 12, 24, 48, 60, 120]
    labels = ["0-12 months", "13-24 months", "25-48 months", "49-60 months", "61+ months"]
    cleaned["TenureGroup"] = pd.cut(cleaned["tenure"], bins=bins, labels=labels)

    # Feature Engineering: AvgMonthlySpend
    cleaned["AvgMonthlySpend"] = np.where(
        cleaned["tenure"] > 0,
        cleaned["TotalCharges"] / cleaned["tenure"],
        cleaned["MonthlyCharges"],
    ).round(2)

    # Convert binary Yes/No columns to 1/0 (preserving Churn_Label for plotting)
    if "Churn" in cleaned.columns:
        cleaned["Churn_Label"] = cleaned["Churn"]
    for col in cleaned.columns:
        unique_vals = set(cleaned[col].dropna().astype(str).unique())
        if unique_vals.issubset({"Yes", "No"}):
            cleaned[col] = cleaned[col].map({"Yes": 1, "No": 0})

    # One-hot encode Contract and InternetService
    ohe_cols = [c for c in ("Contract", "InternetService") if c in cleaned.columns]
    if ohe_cols:
        # Keep original Contract column for EDA barplot under Contract_Label
        if "Contract" in ohe_cols:
            cleaned["Contract_Label"] = cleaned["Contract"]
        cleaned = pd.get_dummies(cleaned, columns=ohe_cols, drop_first=False, dtype=int)

    return cleaned


def generate_visualizations(df: pd.DataFrame) -> None:
    """Create and save required EDA plots."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # 1. Countplot for Churn
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=df, x="Churn_Label", hue="Churn_Label", legend=False, palette="Set2", ax=ax)
    ax.set_title("Customer Churn Distribution")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Customer Count")
    fig.tight_layout()
    fig.savefig(OUTPUTS_DIR / "01_churn_countplot.png", dpi=150)
    plt.close(fig)

    # 2. Barplot: Contract vs Churn
    if "Contract_Label" in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=df, x="Contract_Label", y="Churn", hue="Contract_Label", legend=False, palette="viridis", ax=ax)
        ax.set_title("Churn Rate by Contract Type")
        ax.set_xlabel("Contract Type")
        ax.set_ylabel("Churn Rate")
        fig.tight_layout()
        fig.savefig(OUTPUTS_DIR / "02_contract_vs_churn_barplot.png", dpi=150)
        plt.close(fig)

    # 3. Correlation Heatmap
    num_df = df.select_dtypes(include=[np.number])
    fig, ax = plt.subplots(figsize=(12, 9))
    sns.heatmap(num_df.corr(), cmap="coolwarm", center=0, annot=False, ax=ax)
    ax.set_title("Numeric Feature Correlation Heatmap")
    fig.tight_layout()
    fig.savefig(OUTPUTS_DIR / "03_correlation_heatmap.png", dpi=150)
    plt.close(fig)

    # 4. Boxplot: MonthlyCharges by Churn
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(data=df, x="Churn_Label", y="MonthlyCharges", hue="Churn_Label", legend=False, palette="Set1", ax=ax)
    ax.set_title("Monthly Charges Distribution by Churn")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Monthly Charges ($)")
    fig.tight_layout()
    fig.savefig(OUTPUTS_DIR / "04_monthly_charges_boxplot.png", dpi=150)
    plt.close(fig)

    # 5. Pairplot of key numeric features
    pair_cols = [c for c in ["tenure", "MonthlyCharges", "TotalCharges", "AvgMonthlySpend", "Churn_Label"] if c in df.columns]
    if len(pair_cols) >= 3:
        grid = sns.pairplot(df[pair_cols].sample(min(len(df), 1000), random_state=42), hue="Churn_Label", corner=True)
        grid.fig.suptitle("Pairplot of Key Billing & Tenure Features", y=1.02)
        grid.savefig(OUTPUTS_DIR / "05_churn_pairplot.png", dpi=150)
        plt.close(grid.fig)


def main() -> None:
    csv_path = locate_dataset()
    raw_df = pd.read_csv(csv_path)
    print(f"Loaded dataset: {raw_df.shape[0]} rows, {raw_df.shape[1]} columns")

    cleaned_df = clean_and_engineer_features(raw_df)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(OUTPUTS_DIR / "cleaned_telco_churn.csv", index=False)
    generate_visualizations(cleaned_df)
    print(f"Saved cleaned CSV and visualizations to {OUTPUTS_DIR}")


if __name__ == "__main__":
    main()

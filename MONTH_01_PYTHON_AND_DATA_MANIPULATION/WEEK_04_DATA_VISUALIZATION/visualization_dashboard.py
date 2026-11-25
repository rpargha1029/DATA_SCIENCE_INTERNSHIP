"""Week 4 Hands-On & Client Project: Data Visualization Dashboard with Matplotlib & Seaborn."""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"


def build_sample_dataset(csv_path: Path) -> pd.DataFrame:
    """Create a deterministic synthetic employee & sales performance dataset."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(42)
    n = 120
    experience = rng.uniform(1, 15, n)
    training_hours = rng.uniform(10, 60, n)
    sales = 20 + 4.5 * experience + 0.6 * training_hours + rng.normal(0, 8, n)
    satisfaction = np.clip(3.0 + 0.08 * experience + rng.normal(0, 0.5, n), 1.0, 5.0)
    region = rng.choice(["North", "South", "East", "West"], size=n)

    df = pd.DataFrame(
        {
            "Experience_Years": np.round(experience, 2),
            "Training_Hours": np.round(training_hours, 1),
            "Monthly_Sales_K": np.round(sales, 2),
            "Satisfaction_Score": np.round(satisfaction, 2),
            "Region": region,
        }
    )
    df.to_csv(csv_path, index=False)
    return df


def generate_individual_plots(df: pd.DataFrame) -> None:
    """Generate required Matplotlib & Seaborn plots (histogram, scatter, heatmap, pairplot)."""
    sns.set_theme(style="whitegrid")

    # 1. Histogram of Monthly Sales
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["Monthly_Sales_K"], bins=20, kde=True, color="#2b7bba", ax=ax)
    ax.set_title("Distribution of Monthly Sales ($K)")
    ax.set_xlabel("Monthly Sales ($K)")
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "01_sales_histogram.png", dpi=150)
    plt.close(fig)

    # 2. Scatter plot: Experience vs Monthly Sales by Region
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(
        data=df,
        x="Experience_Years",
        y="Monthly_Sales_K",
        hue="Region",
        palette="viridis",
        s=70,
        alpha=0.85,
        ax=ax,
    )
    ax.set_title("Experience vs Monthly Sales by Region")
    ax.set_xlabel("Experience (Years)")
    ax.set_ylabel("Monthly Sales ($K)")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "02_experience_vs_sales_scatter.png", dpi=150)
    plt.close(fig)

    # 3. Correlation Heatmap
    numeric_cols = ["Experience_Years", "Training_Hours", "Monthly_Sales_K", "Satisfaction_Score"]
    corr = df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(7, 5.5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
    ax.set_title("Feature Correlation Heatmap")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "03_correlation_heatmap.png", dpi=150)
    plt.close(fig)

    # 4. Pairplot
    pair_grid = sns.pairplot(df, hue="Region", corner=True, diag_kind="kde")
    pair_grid.fig.suptitle("Pairwise Feature Relationships by Region", y=1.02)
    pair_grid.savefig(OUTPUT_DIR / "04_feature_pairplot.png", dpi=150)
    plt.close(pair_grid.fig)


def generate_dashboard(df: pd.DataFrame) -> None:
    """Create a 2x2 client visualization dashboard combining key charts."""
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Client Performance & Feature Relationship Dashboard", fontsize=15, fontweight="bold")

    # Top-left: Histogram
    sns.histplot(df["Monthly_Sales_K"], bins=18, kde=True, color="#1f77b4", ax=axes[0, 0])
    axes[0, 0].set_title("Monthly Sales Distribution")

    # Top-right: Scatter plot
    sns.scatterplot(
        data=df, x="Experience_Years", y="Monthly_Sales_K", hue="Region", ax=axes[0, 1], alpha=0.8
    )
    axes[0, 1].set_title("Experience vs. Monthly Sales")

    # Bottom-left: Regional Average Sales Barplot (Matplotlib/Seaborn)
    region_means = df.groupby("Region", as_index=False)["Monthly_Sales_K"].mean().sort_values("Monthly_Sales_K", ascending=False)
    sns.barplot(data=region_means, x="Region", y="Monthly_Sales_K", hue="Region", legend=False, palette="Blues_d", ax=axes[1, 0])
    axes[1, 0].set_title("Average Monthly Sales by Region")

    # Bottom-right: Correlation Heatmap
    corr = df[["Experience_Years", "Training_Hours", "Monthly_Sales_K", "Satisfaction_Score"]].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=axes[1, 1])
    axes[1, 1].set_title("Numeric Feature Correlations")

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUTPUT_DIR / "05_client_visualization_dashboard.png", dpi=150)
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = DATA_DIR / "employee_performance.csv"
    df = build_sample_dataset(csv_path) if not csv_path.exists() else pd.read_csv(csv_path)

    generate_individual_plots(df)
    generate_dashboard(df)
    print(f"Generated 5 visualization files in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

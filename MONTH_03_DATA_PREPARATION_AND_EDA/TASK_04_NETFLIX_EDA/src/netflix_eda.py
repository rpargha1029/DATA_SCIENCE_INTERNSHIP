"""Task 4: Netflix Titles Exploratory Data Analysis & 2-Year Trend Forecast."""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"


def locate_dataset() -> Path:
    """Locate netflix_titles.csv inside data/."""
    for name in ("netflix_titles.csv", "netflix.csv"):
        candidate = DATA_DIR / name
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Netflix Titles CSV not found in {DATA_DIR}.\n"
        "Download from: https://www.kaggle.com/datasets/shivamb/netflix-shows\n"
        f"and save as: {DATA_DIR / 'netflix_titles.csv'}"
    )


def clean_and_engineer(df: pd.DataFrame) -> pd.DataFrame:
    """Clean Netflix metadata and engineer release_decade, is_movie, content_type."""
    cleaned = df.copy()
    cleaned["date_added"] = pd.to_datetime(cleaned["date_added"].astype(str).str.strip(), errors="coerce")
    cleaned["director"] = cleaned["director"].fillna("Unknown")
    cleaned["cast"] = cleaned["cast"].fillna("Unknown")
    cleaned["country"] = cleaned["country"].fillna("Unknown")
    cleaned["rating"] = cleaned["rating"].fillna("Not Rated")

    cleaned["release_year"] = pd.to_numeric(cleaned["release_year"], errors="coerce")
    cleaned = cleaned.dropna(subset=["release_year"]).copy()
    cleaned["release_year"] = cleaned["release_year"].astype(int)

    cleaned["release_decade"] = (cleaned["release_year"] // 10) * 10
    cleaned["content_type"] = cleaned["type"].astype(str).str.strip()
    cleaned["is_movie"] = (cleaned["content_type"] == "Movie").astype(int)
    cleaned["primary_country"] = cleaned["country"].astype(str).str.split(",").str[0].str.strip()
    return cleaned


def get_top_countries(df: pd.DataFrame, top_n: int = 5) -> pd.Series:
    """Return top N countries excluding 'Unknown'."""
    valid = df[df["primary_country"] != "Unknown"]["primary_country"]
    return valid.value_counts().head(top_n)


def generate_visualizations(df: pd.DataFrame) -> dict:
    """Generate 6 EDA & trend forecast visualizations and return summary stats."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # 1. Pie chart: Movie vs TV Shows
    type_counts = df["content_type"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        type_counts.values,
        labels=type_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=["#E50914", "#221F1F"],
        textprops={"color": "black"},
    )
    ax.set_title("Netflix Content Split: Movies vs. TV Shows")
    fig.tight_layout()
    fig.savefig(OUTPUTS_DIR / "01_movie_vs_tv_pie.png", dpi=150)
    plt.close(fig)

    # 2. Line plot: Content released per year
    yearly = df.groupby("release_year").size().reset_index(name="Count")
    recent_yearly = yearly[yearly["release_year"] >= 2000]
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.lineplot(data=recent_yearly, x="release_year", y="Count", marker="o", color="#E50914", ax=ax)
    ax.set_title("Netflix Titles Released per Year (2000+)")
    ax.set_xlabel("Release Year")
    ax.set_ylabel("Number of Titles")
    fig.tight_layout()
    fig.savefig(OUTPUTS_DIR / "02_content_released_per_year.png", dpi=150)
    plt.close(fig)

    # 3. Barplot: Top 10 genres
    genres = (
        df["listed_in"]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=genres.values, y=genres.index, hue=genres.index, legend=False, palette="Reds_r", ax=ax)
    ax.set_title("Top 10 Genres on Netflix")
    ax.set_xlabel("Title Count")
    ax.set_ylabel("Genre")
    fig.tight_layout()
    fig.savefig(OUTPUTS_DIR / "03_top_10_genres_barplot.png", dpi=150)
    plt.close(fig)

    # 4. Barplot: Top 5 Countries
    top_countries = get_top_countries(df, top_n=5)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(x=top_countries.index, y=top_countries.values, hue=top_countries.index, legend=False, palette="dark:salmon_r", ax=ax)
    ax.set_title("Top 5 Content-Producing Countries on Netflix")
    ax.set_xlabel("Country")
    ax.set_ylabel("Number of Titles")
    fig.tight_layout()
    fig.savefig(OUTPUTS_DIR / "04_top_5_countries.png", dpi=150)
    plt.close(fig)

    # 5. Heatmap: Country vs Content Type Volume
    top5_names = list(top_countries.index)
    country_type_ct = pd.crosstab(
        df[df["primary_country"].isin(top5_names)]["primary_country"],
        df["content_type"],
    )
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(country_type_ct, annot=True, fmt="d", cmap="YlOrRd", ax=ax)
    ax.set_title("Top 5 Countries vs. Content Type Volume")
    ax.set_xlabel("Content Type")
    ax.set_ylabel("Country")
    fig.tight_layout()
    fig.savefig(OUTPUTS_DIR / "05_country_content_heatmap.png", dpi=150)
    plt.close(fig)

    # 6. Bonus: 2-year trend prediction based on last 8 years of additions/releases
    trend_df = yearly[(yearly["release_year"] >= yearly["release_year"].max() - 8) & (yearly["release_year"] < yearly["release_year"].max())]
    forecast_info = {}
    if len(trend_df) >= 3:
        reg = LinearRegression()
        X_years = trend_df[["release_year"]].values
        y_counts = trend_df["Count"].values
        reg.fit(X_years, y_counts)
        max_yr = int(yearly["release_year"].max())
        future_years = np.array([[max_yr + 1], [max_yr + 2]])
        preds = np.maximum(0, np.round(reg.predict(future_years))).astype(int)
        forecast_info = {int(future_years[0][0]): int(preds[0]), int(future_years[1][0]): int(preds[1])}

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(trend_df["release_year"], y_counts, marker="o", label="Historical Releases", color="#221F1F")
        ax.plot(
            [trend_df["release_year"].iloc[-1], future_years[0][0], future_years[1][0]],
            [y_counts[-1], preds[0], preds[1]],
            marker="s",
            linestyle="--",
            color="#E50914",
            label="2-Year Linear Forecast",
        )
        ax.set_title("Bonus: 2-Year Content Release Trend Forecast")
        ax.set_xlabel("Year")
        ax.set_ylabel("Title Count")
        ax.legend()
        fig.tight_layout()
        fig.savefig(OUTPUTS_DIR / "06_two_year_trend_forecast.png", dpi=150)
        plt.close(fig)

    return {"type_counts": type_counts.to_dict(), "top_countries": top_countries.to_dict(), "forecast": forecast_info}


def main() -> None:
    csv_path = locate_dataset()
    raw_df = pd.read_csv(csv_path)
    print(f"Loaded Netflix dataset: {raw_df.shape[0]} rows, {raw_df.shape[1]} columns")
    cleaned_df = clean_and_engineer(raw_df)
    stats = generate_visualizations(cleaned_df)
    print("Generated 6 visualizations in:", OUTPUTS_DIR)
    print("Summary stats:", stats)


if __name__ == "__main__":
    main()

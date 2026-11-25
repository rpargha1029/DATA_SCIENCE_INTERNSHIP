"""Month 4: Content-Based Movie Recommendation System (TMDB 5000)."""

import ast
from pathlib import Path
import pickle
import re
from typing import List, Tuple

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"


def locate_datasets() -> Tuple[Path, Path]:
    """Locate tmdb_5000_movies.csv and tmdb_5000_credits.csv in data/."""
    movies_path = DATA_DIR / "tmdb_5000_movies.csv"
    credits_path = DATA_DIR / "tmdb_5000_credits.csv"
    if not movies_path.exists() or not credits_path.exists():
        raise FileNotFoundError(
            f"TMDB 5000 CSVs not found in {DATA_DIR}.\n"
            "Download from: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata\n"
            f"Place 'tmdb_5000_movies.csv' and 'tmdb_5000_credits.csv' in {DATA_DIR}"
        )
    return movies_path, credits_path


def _parse_names(json_str: str, limit: int | None = None) -> List[str]:
    """Extract 'name' fields from a JSON-like list string, removing internal spaces."""
    if pd.isna(json_str):
        return []
    try:
        items = ast.literal_eval(str(json_str))
    except (ValueError, SyntaxError):
        return []
    names = [str(item.get("name", "")).replace(" ", "") for item in items if isinstance(item, dict)]
    return names[:limit] if limit else names


def clean_text(text: str) -> str:
    """Lowercase text and remove punctuation."""
    lowered = str(text).lower()
    return re.sub(r"[^\w\s]", " ", lowered).strip()


def prepare_movie_tags(movies_df: pd.DataFrame, credits_df: pd.DataFrame) -> pd.DataFrame:
    """Merge movies and credits and construct cleaned 'tags' column."""
    merged = movies_df.merge(credits_df, on="title", how="inner")
    id_col = "movie_id" if "movie_id" in merged.columns else "id"
    df = merged[[id_col, "title", "overview", "genres", "keywords", "cast"]].copy()
    df = df.rename(columns={id_col: "movie_id"})
    df["overview"] = df["overview"].fillna("")

    df["genres_list"] = df["genres"].apply(_parse_names)
    df["keywords_list"] = df["keywords"].apply(_parse_names)
    df["cast_list"] = df["cast"].apply(lambda x: _parse_names(x, limit=5))

    df["tags"] = (
        df["overview"]
        + " "
        + df["genres_list"].apply(" ".join)
        + " "
        + df["keywords_list"].apply(" ".join)
        + " "
        + df["cast_list"].apply(" ".join)
    ).apply(clean_text)

    result = df[["movie_id", "title", "tags"]].drop_duplicates(subset=["title"]).reset_index(drop=True)
    return result


def build_and_save_model(movies_clean: pd.DataFrame, save_artifacts: bool = True):
    """Fit TfidfVectorizer, compute cosine similarity, and optionally pickle artifacts."""
    vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
    vectors = vectorizer.fit_transform(movies_clean["tags"])
    similarity = cosine_similarity(vectors)

    if save_artifacts:
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        with open(MODELS_DIR / "vectorizer.pkl", "wb") as f:
            pickle.dump(vectorizer, f)
        with open(MODELS_DIR / "similarity_matrix.pkl", "wb") as f:
            pickle.dump(similarity, f)
        with open(MODELS_DIR / "movies_metadata.pkl", "wb") as f:
            pickle.dump(movies_clean[["movie_id", "title", "tags"]], f)

    return vectorizer, similarity


def recommend(title: str, movies_df: pd.DataFrame, similarity_matrix, top_n: int = 5) -> List[Tuple[str, float]]:
    """Return top_n similar movies for a given title with case-insensitive validation."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Movie title must be a non-empty string.")

    query = title.strip().lower()
    lower_titles = movies_df["title"].str.lower()
    matches = movies_df.index[lower_titles == query].tolist()

    if not matches:
        partial = movies_df[lower_titles.str.contains(re.escape(query), na=False)]["title"].head(5).tolist()
        hint = f" Did you mean: {partial}?" if partial else ""
        raise ValueError(f"Movie '{title}' not found in dataset.{hint}")

    idx = matches[0]
    scores = list(enumerate(similarity_matrix[idx]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommendations = []
    for movie_idx, score in sorted_scores[1 : top_n + 1]:
        recommendations.append((str(movies_df.iloc[movie_idx]["title"]), round(float(score), 4)))
    return recommendations


def main() -> None:
    movies_path, credits_path = locate_datasets()
    movies_df = pd.read_csv(movies_path)
    credits_df = pd.read_csv(credits_path)
    movies_clean = prepare_movie_tags(movies_df, credits_df)
    _, similarity = build_and_save_model(movies_clean, save_artifacts=True)

    sample_title = str(movies_clean.iloc[0]["title"])
    print(f"Saved recommender artifacts to {MODELS_DIR}")
    print(f"Top 5 recommendations for '{sample_title}':")
    for rec_title, score in recommend(sample_title, movies_clean, similarity):
        print(f"  - {rec_title} (similarity={score:.4f})")


if __name__ == "__main__":
    main()

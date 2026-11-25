"""Optional Streamlit App for Content-Based Movie Recommendation System."""

import os
from pathlib import Path
import pickle
import sys

import requests
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.recommender import recommend  # type: ignore[import-not-found]


st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")


@st.cache_resource
def load_artifacts():
    with open(MODELS_DIR / "movies_metadata.pkl", "rb") as f:
        movies_df = pickle.load(f)
    with open(MODELS_DIR / "similarity_matrix.pkl", "rb") as f:
        similarity = pickle.load(f)
    return movies_df, similarity


def fetch_poster_url(movie_id: int) -> str | None:
    """Fetch TMDB poster URL if TMDB_API_KEY is configured; otherwise return None."""
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        return None
    try:
        resp = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            params={"api_key": api_key},
            timeout=5,
        )
        if resp.status_code == 200:
            poster_path = resp.json().get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except requests.RequestException:
        pass
    return None


def main() -> None:
    st.title("Content-Based Movie Recommendation System")
    st.write("Enter or select a movie title to discover the top 5 most similar films.")

    if not (MODELS_DIR / "movies_metadata.pkl").exists():
        st.error("Model artifacts not found. Run `python src/recommender.py` first after downloading the TMDB 5000 dataset.")
        return

    movies_df, similarity = load_artifacts()
    query_title = st.text_input("Search movie title", value=str(movies_df.iloc[0]["title"]))

    if st.button("Recommend"):
        try:
            recs = recommend(query_title, movies_df, similarity, top_n=5)
            cols = st.columns(5)
            for col, (title, score) in zip(cols, recs):
                with col:
                    movie_id = int(movies_df.loc[movies_df["title"] == title, "movie_id"].iloc[0])
                    poster = fetch_poster_url(movie_id)
                    if poster:
                        st.image(poster, width="stretch")
                    else:
                        st.info("Poster unavailable (set TMDB_API_KEY to load posters)")
                    st.subheader(title)
                    st.caption(f"Cosine Similarity: {score:.4f}")
        except ValueError as exc:
            st.warning(str(exc))


if __name__ == "__main__":
    main()

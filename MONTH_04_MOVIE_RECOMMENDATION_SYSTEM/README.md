# Month 4: Content-Based Movie Recommendation System

## Objective
Build a content-based movie recommender engine using movie descriptions (`overview`), `genres`, `keywords`, and `cast` with text vectorization and cosine similarity, plus an optional Streamlit web interface.

## Tasks Implemented
- **Data Cleaning & Tag Construction**:
  - Parse JSON-formatted `genres`, `keywords`, and top-5 `cast` names from the TMDB 5000 dataset.
  - Combine `overview`, `genres`, `keywords`, and `cast` into a unified `tags` column.
  - Convert text to lowercase and strip punctuation.
- **Vectorization & Similarity**:
  - Vectorize `tags` using `TfidfVectorizer(max_features=5000, stop_words="english")`.
  - Compute pairwise cosine similarity matrix across all movies.
- **Recommendation Logic**:
  - `recommend(title, top_n=5)` returns the top 5 most similar movies with case-insensitive input validation.
- **Model Persistence**:
  - Saves `vectorizer.pkl`, `similarity_matrix.pkl`, and `movies_metadata.pkl` in `models/`.
- **Optional Streamlit App**:
  - `app/streamlit_app.py` provides an interactive movie search box and displays top 5 recommendations (with optional TMDB poster lookup via `TMDB_API_KEY` env var and clean fallback cards).

## Dataset Source & Manual Download
- **Dataset**: TMDB 5000 Movie Dataset (Kaggle)
- **URL**: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
- **Setup**: Download `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` and place both in `MONTH_04_MOVIE_RECOMMENDATION_SYSTEM/data/`.

## Execution
```bash
# 1. Build vectorizer, similarity matrix, and test recommendations
python src/recommender.py

# 2. Launch optional Streamlit app
streamlit run app/streamlit_app.py
```

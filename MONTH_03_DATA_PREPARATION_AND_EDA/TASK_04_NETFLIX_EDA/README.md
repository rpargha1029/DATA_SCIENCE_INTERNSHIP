# Task 4: Netflix Titles Dataset — Exploratory Analysis & Insights

## Objective
Explore Netflix media content metadata to identify viewing trends, content type distributions, top genres, popular countries, and a 2-year content volume trend forecast.

## Tasks Implemented
- **Data Understanding & Cleaning**:
  - Convert `date_added` to `datetime`.
  - Fill missing values in `director`, `cast`, and `country` with `"Unknown"`.
  - Create `release_decade` and `is_movie` features.
- **Feature Engineering**:
  - Extract `release_year`, `content_type` (`Movie` / `TV Show`), and top 5 countries by title count.
  - Parse multi-label columns (`listed_in` genres, `country`).
- **Visualization & Insights (6 visuals)**:
  1. Pie chart: Movies vs. TV Shows.
  2. Line plot: Content released per year.
  3. Barplot: Top 10 genres (`listed_in`).
  4. Heatmap: Top 5 countries vs. content volume (`Movie` vs `TV Show`).
  5. Barplot: Top 5 content-producing countries.
  6. Bonus: 2-year release/addition trend prediction using linear regression.
- **Deliverables**: Jupyter notebook (`notebooks/netflix_eda.ipynb`), Python script (`src/netflix_eda.py`), 6 PNG visuals in `outputs/`, and `outputs/INSIGHTS_SUMMARY.md`.

## Dataset Source & Manual Download
- **Dataset**: Netflix Movies and TV Shows (Kaggle, ~8,807 rows)
- **URL**: https://www.kaggle.com/datasets/shivamb/netflix-shows
- **Setup**: Download `netflix_titles.csv` and place it in `TASK_04_NETFLIX_EDA/data/`.

## Execution
```bash
python src/netflix_eda.py
```

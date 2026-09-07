# 📖🎬 ReadWatch Analyzer

A tool for analyzing your personal reading and movie-watching history. Import your Goodreads library export and Letterboxd data exports into a local SQLite database, then explore stats about your reading and watching habits — ratings, pace, streaks, and more — through a CLI or a visual dashboard.

**[Live Dashboard →]([your-deployed-url-here](https://shamas9149-readwatch-analyzer-dashboard-x62kur.streamlit.app/))**

## Features

**Books (Goodreads)**
- Total books read, average rating, total pages read
- 5-star favorites
- Book lookups enriched with cover images and publish year via the [Open Library API](https://openlibrary.org/developers/api)

**Movies (Letterboxd)**
- Movies watched count, average rating
- 5-star favorites
- Random pick from your watchlist
- Busiest movie month / year-by-year breakdown
- Longest gap without watching anything

**Dashboard**
- Visual stats view built with [Streamlit](https://streamlit.io)
- Side-by-side metrics, 5-star lists, and a "surprise me" watchlist button

## Tech Stack

- Python
- SQLite (`sqlite3`)
- `requests` for API calls
- Streamlit for the dashboard

## How It Works

1. Export your library data:
   - Goodreads: **My Books → Import/Export → Export Library**
   - Letterboxd: **Settings → Import & Export → Export Data**
2. Place the CSV files in the project folder
3. Run `main.py` — it imports the CSVs into `books.db` and `movies.db` (only on first run) and opens an interactive CLI menu
4. Run `streamlit run dashboard.py` to view the visual dashboard

## Setup

```bash
pip install requests streamlit
python main.py
```

To view the dashboard:
```bash
streamlit run dashboard.py
```

## What I Learned

This project was built to practice:
- Reading and cleaning real-world CSV data
- Designing a SQLite schema and writing SQL (`WHERE`, `GROUP BY`, `ORDER BY`, `AVG`, aliasing)
- Making real API calls, handling errors, timeouts, and rate limits
- Building a simple data dashboard with Streamlit
- Git/GitHub version control

## Notes

- Goodreads' public API was discontinued in 2020, so this project uses their CSV export instead
- Letterboxd has no official public API; CSV export is the standard method

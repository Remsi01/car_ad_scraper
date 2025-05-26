# 🚗 Finn.no Car Scraper

This project is a Python-based web scraper that extracts car listings from [finn.no](https://www.finn.no/), Filters out suspicious listings (monthly payments) with prices that are too low for the given year and mileage.The scraper runs periodically (every 15 minutes), stores data in JSON format, and generates a ranked list of cars for analysis.

Built with Playwright for headless web scraping, pandas for data processing.

---

## 🌟 Features

- **Scraping**: Extracts car listings from Finn.no, including title, price, year, mileage, transmission, fuel, location, and ad ID.
- **Filtering**: Identifies and skips suspicious listings (e.g., price ≤ 15,000 NOK, year ≥ 2019, mileage ≤ 100,000 km) with monthly payment terms.
- **Periodic Execution**: Runs every 15 minutes to fetch new ads and avoid duplicates.
- **Data Management**: Stores data in `data/finn_cars.json`, trimming to the last 10,000 entries.
- **Ranking**: Ranks cars based on a weighted score (`score = Year.rank(ascending=False) + Mileage.rank(ascending=True) + Price.rank(ascending=True) * 10`) and saves results to `data/sorted_cars.json` and `docs/sorted_cars.json`.
- **Logging**: Uses rotating logs (`logs/main.log`, 5MB, 5 backups) for debugging and monitoring, with terminal output.
- **Frontend**: Displays ranked listings in a table via a static HTML/JS viewer hosted on GitHub Pages.

---

## 🗂️ Project Structure

```bash
finn_scraper/
├── main.py                    # Orchestrates scraping and saving
├── data/
│   ├── finn_cars.json         # Full dataset of scraped ads (latest 10k entries)
│   └── sorted_cars.json       # Ranked results (top 20k entries)
├── docs/                      # GitHub Pages frontend (viewer UI + JSON)
│   ├── sorted_cars.json       # Synced JSON for frontend
│   └── index.html             # Frontend viewer
├── logs/
│   └── main.log               # Rotating log of scraper activity
├── src/
│   ├── scraper.py             # Playwright-based scraper
│   ├── data_handler.py        # Saves and triggers ranking
│   └── finn_cars_best_match.py # Scoring and ranking script
├── requirements.txt           # Python dependencies
└── README.md                  # You're here!
```

---

## 🛠️ Prerequisites

- Python 3.10+
- Playwright (headless browser automation)
- Pandas (data analysis)

---

## 🔧 Setup Instructions

1. **Clone the repo**:
   ```bash
   git clone https://github.com/Remsi01/car_ad_scraper
   cd car_ad_scraper
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install  # Installs browser binaries for Playwright
   ```

4. **Run the scraper loop**:
   ```bash
   python main.py
   ```
   - The scraper runs every 15 minutes. Stop it with `Ctrl+C`.
   - Check logs in `logs/main.log` for debugging.

5. **View output**:
   - Ranked listings in `data/sorted_cars.json`.
   - Serve the frontend via GitHub Pages or locally by opening `docs/index.html` in a browser (ensure `docs/sorted_cars.json` is populated).

6. **Optional: Set up GitHub Pages**:
   - Push the `docs/` folder to a GitHub repository.
   - Enable GitHub Pages in the repository settings, selecting the `docs` folder as the source.

---

## 🧪 Sample Output (JSON format)

```json
{
  "Annonse ID": "123456789",
  "Title": "Toyota Yaris 2020",
  "Price": 89000,
  "Year": 2020,
  "Mileage": 67000,
  "Transmission": "Automatic",
  "Fuel": "Petrol",
  "Location": "Oslo",
  "No": 54321,
  "score": 1234.5
}
```


---

## 🔐 Disclaimer

This tool is intended for educational and research purposes only. It respects finn.no's fair use policies. No scraping of user data or personal information is involved.
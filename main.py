import os
import json
import time
import logging
from logging.handlers import RotatingFileHandler

from src.scraper import scrape_finn_cars
from src.data_handler import save_data

# Constants
DATA_FILE = "data/finn_cars.json"
INTERVAL_MINUTES = 15

# Logging setup
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "main.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Configure rotating file logger (5MB per file, keep last 5 logs)
rotating_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=5,
    encoding="utf-8"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        rotating_handler,
        logging.StreamHandler()  # Enables terminal logging
    ]
)

def load_existing_data(filename=DATA_FILE):
    """
    Load previously scraped ads from the JSON file, if it exists and is valid.
    Returns a list of ads or an empty list if the file is missing or invalid.
    """
    if not os.path.exists(filename):
        logging.info(f"ℹ️ Data file '{filename}' not found. Starting with empty data.")
        return []

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                logging.warning(f"⚠️ Data file '{filename}' is empty. Starting with empty data.")
                return []
            return json.loads(content)
    except json.JSONDecodeError as e:
        logging.error(f"⚠️ Invalid JSON in '{filename}': {e}. Starting with empty data.")
        return []
    except Exception as e:
        logging.error(f"⚠️ Error reading '{filename}': {e}. Starting with empty data.")
        return []

def run_loop():
    """
    Main loop that periodically scrapes new car ads from finn.no,
    appends unseen ads to the dataset, and saves to disk.
    """
    all_ads = load_existing_data()
    known_ids = {item["Annonse ID"] for item in all_ads}
    last_no = max((item.get("No", 0) for item in all_ads), default=0)

    logging.info(f"🔁 Scraping every {INTERVAL_MINUTES} min. Press Ctrl+C to stop.")

    try:
        while True:
            logging.info("\n⏳ Scraping new data...")
            new_ads = scrape_finn_cars(return_data=True)
            added = 0

            # Add only new ads
            for ad in new_ads:
                if ad["Annonse ID"] not in known_ids:
                    last_no += 1
                    ad["No"] = last_no
                    all_ads.append(ad)
                    known_ids.add(ad["Annonse ID"])
                    added += 1

            logging.info(f"🆕 Added {added} new ads.")

            # Save the updated data (save_data handles truncation and further processing)
            save_data(all_ads)

            # Wait for the next scraping interval
            #print(f"Sleeping for {INTERVAL_MINUTES} min.")
            logging.info(f"Sleeping for {INTERVAL_MINUTES} min.")
            time.sleep(INTERVAL_MINUTES * 60)
    except KeyboardInterrupt:
        logging.warning("\n❌ Scraper stopped by user.")

if __name__ == "__main__":
    run_loop()

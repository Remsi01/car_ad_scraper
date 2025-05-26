# src/data_handler.py

import json
import subprocess
import logging
import sys
import os

# Define base and data paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'finn_cars.json')

def save_data(data, max_entries=10000):
    """
    Save a list of car ads to a JSON file, trim to last N entries,
    and trigger best-match ranking script.
    """
    if not isinstance(data, list):
        logging.error("❌ Provided data is not a list. Aborting save.")
        return

    # Sort by 'No' field (a serial number)
    data = sorted(data, key=lambda x: x.get("No", 0))

    # Trim to last max_entries
    if len(data) > max_entries:
        data = data[-max_entries:]

    # Ensure output directory exists
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    try:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logging.info(f"💾 Saved {len(data)} entries to '{DATA_PATH}'")
    except Exception as e:
        logging.error(f"❌ Failed to write data to file: {e}")
        return

    # Run the best-match ranking script
    try:
        best_match_script = os.path.join(BASE_DIR, 'src', 'finn_cars_best_match.py')
        subprocess.run([sys.executable, best_match_script], check=True)
        logging.info("📊 Best-match analysis completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Error running best-match script: {e}")
    except Exception as e:
        logging.error(f"❌ Unexpected error when launching best-match script: {e}")

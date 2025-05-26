# src/finn_cars_best_match.py

import logging
import sys
import os
import pandas as pd
import json

# Set up paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'finn_cars.json')
OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'sorted_cars.json')
DOCS_OUTPUT_PATH = os.path.join(BASE_DIR, 'docs', 'sorted_cars.json')

def load_data(path):
    """
    Load data from a JSON file.
    """
    if not os.path.exists(path):
        logging.error(f"❌ Error: '{path}' does not exist. Run main.py to generate it.")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_and_score(df):
    """
    Clean and rank car listings using a score based on:
    - Lower price (10x weight)
    - Lower mileage
    - Higher year
    """
    df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'\D', '', regex=True), errors='coerce')
    df['Mileage'] = pd.to_numeric(df['Mileage'].astype(str).str.replace(r'\D', '', regex=True), errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    df.dropna(subset=['Year', 'Price', 'Mileage'], inplace=True)

    df['score'] = (
        df['Year'].rank(ascending=False) +
        df['Mileage'].rank(ascending=True) +
        df['Price'].rank(ascending=True) * 10  # Price has more influence
    )

    return df.sort_values(by='score').head(20000)

def save_json(data, path):
    """
    Save data to a JSON file with formatting.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    try:
        # Step 1: Load and parse data
        raw_data = load_data(DATA_PATH)
        df = pd.DataFrame(raw_data)

        # Step 2: Clean and rank listings
        df_sorted = clean_and_score(df)
        sorted_records = df_sorted.to_dict(orient='records')

        # Step 3: Save results
        save_json(sorted_records, OUTPUT_PATH)
        save_json(sorted_records, DOCS_OUTPUT_PATH)

        logging.info(f"✅ Saved top {len(sorted_records)} best-matched ads to '{OUTPUT_PATH}' and '{DOCS_OUTPUT_PATH}'")
    except Exception as e:
        logging.error(f"❌ Error in best-match analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

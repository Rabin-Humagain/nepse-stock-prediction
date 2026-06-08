import os
from datetime import date
from daily_scraper import scrape_today, append_to_history, save_daily_snapshot
from clean import clean_all
from filter_usable import filter_usable
from predict import predict_all

def run_pipeline():
    print("=" * 40)
    print(f"  NEPSE Daily Pipeline — {date.today()}")
    print("=" * 40)

    print("\n[1/4] Scraping today's prices...")
    df = scrape_today()
    append_to_history(df)
    save_daily_snapshot(df)

    print("\n[2/4] Cleaning data...")
    clean_all()

    print("\n[3/4] Filtering usable companies...")
    filter_usable()

    print("\n[4/4] Running predictions...")
    predict_all()

    print("\n" + "=" * 40)
    print(f"  Done! Predictions saved to:")
    print(f"  data/predictions/{date.today()}.csv")
    print("=" * 40)

if __name__ == "__main__":
    run_pipeline()
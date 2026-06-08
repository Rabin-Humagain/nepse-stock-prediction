import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import urllib3
from datetime import date

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

def scrape_today():
    url = "https://www.sharesansar.com/today-share-price"
    response = requests.get(url, headers=HEADERS, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "headFixed"})

    if not table:
        print("Table not found — market may be closed today")
        return None

    rows = table.find_all("tr")[1:]
    data = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 6:
            data.append({
                "date":       str(date.today()),
                "symbol":     cols[1].text.strip(),
                "prev_close": cols[2].text.strip(),
                "open":       cols[3].text.strip(),
                "high":       cols[4].text.strip(),
                "low":        cols[5].text.strip(),
                "close":      cols[6].text.strip(),
                "volume":     cols[13].text.strip(),
            })

    if not data:
        print("No data found — market may be closed today")
        return None

    df = pd.DataFrame(data)
    print(f"Fetched {len(df)} stocks for {date.today()}")
    return df


def append_to_history(df):
    if df is None:
        return

    updated = 0
    skipped = 0
    errors = 0

    os.makedirs(os.path.join("data", "history"), exist_ok=True)

    for _, row in df.iterrows():
        try:
            # clean symbol — strip whitespace and special characters
            symbol = str(row["symbol"]).strip()
            symbol = "".join(c for c in symbol if c.isalnum())

            if not symbol:
                continue

            filepath = os.path.join("data", "history", symbol + ".csv")

            new_row = pd.DataFrame([{
                "date":   row["date"],
                "open":   row["open"],
                "high":   row["high"],
                "low":    row["low"],
                "close":  row["close"],
                "volume": row["volume"],
            }])

            if os.path.exists(filepath):
                existing = pd.read_csv(filepath)
                if str(row["date"]) in existing["date"].values:
                    skipped += 1
                    continue
                updated_df = pd.concat([new_row, existing], ignore_index=True)
                updated_df.to_csv(filepath, index=False)
            else:
                new_row.to_csv(filepath, index=False)

            updated += 1

        except Exception as e:
            errors += 1
            continue

    print(f"Updated: {updated} | Skipped: {skipped} | Errors: {errors}")


def save_daily_snapshot(df):
    if df is None:
        return

    os.makedirs(os.path.join("data", "daily"), exist_ok=True)
    filepath = os.path.join("data", "daily", f"{date.today()}.csv")

    if os.path.exists(filepath):
        print(f"Snapshot for {date.today()} already exists — skipping")
        return

    df.to_csv(filepath, index=False)
    print(f"Snapshot saved to data/daily/{date.today()}.csv")


if __name__ == "__main__":
    print(f"Running daily scraper for {date.today()}...\n")
    df = scrape_today()
    append_to_history(df)
    save_daily_snapshot(df)
    print("\nDone!")
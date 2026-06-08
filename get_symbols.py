import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_all_symbols():
    url = "https://www.sharesansar.com/today-share-price"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}

    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "headFixed"})

    rows = table.find_all("tr")[1:]
    data = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 6:
            data.append({
                "symbol":     cols[1].text.strip(),
                "ltp":        cols[6].text.strip(),   # last traded price
                "open":       cols[3].text.strip(),
                "high":       cols[4].text.strip(),
                "low":        cols[5].text.strip(),
                "volume":     cols[13].text.strip(),
                "prev_close": cols[2].text.strip(),
            })

    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/all_symbols.csv", index=False)
    print(f"Found {len(df)} companies")
    print(df.head(5))
    return df

if __name__ == "__main__":
    get_all_symbols()
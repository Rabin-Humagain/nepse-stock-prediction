import pandas as pd
import os
import time
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def get_table_rows(driver):
    table = driver.find_element(By.ID, "myTableCPriceHistory")
    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 6:
            data.append({
                "date":   cols[1].text.strip(),
                "open":   cols[2].text.strip(),
                "high":   cols[3].text.strip(),
                "low":    cols[4].text.strip(),
                "close":  cols[5].text.strip(),
                "volume": cols[6].text.strip() if len(cols) > 6 else "",
            })
    return data


def scrape_history(driver, symbol):
    url = f"https://www.sharesansar.com/company/{symbol}"
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    try:
        tab = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a[href='#cpricehistory']")
        ))
        driver.execute_script("arguments[0].click();", tab)

        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#myTableCPriceHistory tbody tr")
        ))

        all_data = []
        page = 1

        while True:
            print(f"  [{symbol}] Page {page}...", end=" ")
            rows = get_table_rows(driver)
            print(f"{len(rows)} rows")
            all_data.extend(rows)

            try:
                next_btn = driver.find_element(
                    By.CSS_SELECTOR, "#myTableCPriceHistory_next"
                )
                if "disabled" in next_btn.get_attribute("class"):
                    print(f"  [{symbol}] Last page reached")
                    break

                driver.execute_script("arguments[0].click();", next_btn)
                time.sleep(1.5)
                page += 1

                if page > 55:
                    break

            except Exception:
                print(f"  [{symbol}] No next button found")
                break

        if not all_data:
            print(f"  [{symbol}] No data")
            return

        df = pd.DataFrame(all_data)
        os.makedirs("data/history", exist_ok=True)
        df.to_csv(f"data/history/{symbol}.csv", index=False)
        print(f"  [{symbol}] Done — {len(df)} total rows saved")

    except Exception as e:
        print(f"  [{symbol}] Error: {e}")


def scrape_all():
    symbols_df = pd.read_csv("data/all_symbols.csv")
    symbols = symbols_df["symbol"].dropna().tolist()
    print(f"Scraping {len(symbols)} companies...\n")

    # log file to track progress
    log_path = "data/scrape_log.txt"

    driver = create_driver()
    try:
        for i, symbol in enumerate(symbols):
            if os.path.exists(f"data/history/{symbol}.csv"):
                print(f"[{i+1}/{len(symbols)}] {symbol} — skipping")
                continue

            print(f"\n[{i+1}/{len(symbols)}] {symbol}")
            try:
                scrape_history(driver, symbol)
                # log success
                with open(log_path, "a") as log:
                    log.write(f"OK: {symbol}\n")
            except Exception as e:
                # log failure
                with open(log_path, "a") as log:
                    log.write(f"FAIL: {symbol} — {e}\n")
                # restart driver in case it crashed
                try:
                    driver.quit()
                except:
                    pass
                driver = create_driver()

    finally:
        driver.quit()

    print("\nAll done!")


if __name__ == "__main__":
    scrape_all()
    time.sleep(random.uniform(3, 7))
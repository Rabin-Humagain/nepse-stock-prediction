import pandas as pd
import os


def clean_dataframe(df, symbol):
    for col in ["open", "high", "low", "close"]:
        if col in df.columns:
            df[col] = df[col].astype(str)
            df[col] = df[col].str.replace(",", "", regex=False)
            df[col] = df[col].str.replace(" ", "", regex=False)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # drop volume entirely — was scraped incorrectly
    if "volume" in df.columns:
        df = df.drop(columns=["volume"])

    # prices can never be negative or zero
    for col in ["open", "high", "low", "close"]:
        if col in df.columns:
            df = df[df[col] > 0]

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "close"])
    df = df.drop_duplicates(subset=["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["symbol"] = symbol

    return df


def clean_all():
    history_dir = "data/history"
    cleaned_dir = "data/cleaned"
    os.makedirs(cleaned_dir, exist_ok=True)

    files = os.listdir(history_dir)
    print(f"Cleaning {len(files)} companies...\n")

    total_dropped = 0
    failed = []

    for i, f in enumerate(files):
        symbol = f.replace(".csv", "")
        filepath = f"{history_dir}/{f}"

        try:
            df = pd.read_csv(filepath)

            if df.empty:
                failed.append(symbol)
                continue

            original_len = len(df)
            df = clean_dataframe(df, symbol)
            dropped = original_len - len(df)
            total_dropped += dropped

            df.to_csv(f"{cleaned_dir}/{symbol}.csv", index=False)

            if (i + 1) % 50 == 0:
                print(f"[{i+1}/{len(files)}] done so far...")

        except Exception as e:
            print(f"Failed: {symbol} — {e}")
            failed.append(symbol)

    print(f"\nCleaning done!")
    print(f"Total rows dropped: {total_dropped}")
    print(f"Failed companies: {len(failed)}")
    if failed:
        print(failed)


if __name__ == "__main__":
    clean_all()
import os
import pandas as pd

def filter_usable():
    cleaned_dir = "data/cleaned"
    usable_dir = "data/usable"
    os.makedirs(usable_dir, exist_ok=True)

    files = os.listdir(cleaned_dir)
    usable = 0
    skipped = 0

    for f in files:
        df = pd.read_csv(f"{cleaned_dir}/{f}")
        if len(df) >= 100:
            df.to_csv(f"{usable_dir}/{f}", index=False)
            usable += 1
        else:
            skipped += 1

    print(f"Usable: {usable} | Skipped: {skipped}")

if __name__ == "__main__":
    filter_usable()
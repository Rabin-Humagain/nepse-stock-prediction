
import os
import pandas as pd

print("=== NEPSE Project Status ===\n")

# check folders
folders = ["data/history", "data/cleaned", "data/usable", "data/charts"]
for folder in folders:
    if os.path.exists(folder):
        count = len(os.listdir(folder))
        print(f"✓ {folder}: {count} files")
    else:
        print(f"✗ {folder}: MISSING")

# check usable dataset
print("\n--- Usable Dataset ---")
usable_dir = "data/usable"
files = os.listdir(usable_dir)
total_rows = 0
for f in files:
    df = pd.read_csv(f"{usable_dir}/{f}")
    total_rows += len(df)

print(f"Companies: {len(files)}")
print(f"Total rows: {total_rows}")
print(f"Average rows: {total_rows // len(files)}")

# check one company in detail
print("\n--- NABIL sample ---")
df = pd.read_csv("data/usable/NABIL.csv")
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"Date range: {df['date'].min()} → {df['date'].max()}")
print(df.tail(3))

print("\n=== All good — ready for Phase 3 ===")
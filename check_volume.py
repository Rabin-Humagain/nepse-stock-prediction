import pandas as pd

df = pd.read_csv("data/history/NABIL.csv")
print("Raw volume samples:")
print(df["volume"].head(20).tolist())
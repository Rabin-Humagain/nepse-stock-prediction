import pandas as pd
import os

def add_features(df):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # price change from previous day
    df["price_change"]  = df["close"].pct_change()

    # moving averages
    df["ma7"]           = df["close"].rolling(7).mean()
    df["ma20"]          = df["close"].rolling(20).mean()
    df["ma50"]          = df["close"].rolling(50).mean()

    # price relative to moving averages
    df["close_to_ma7"]  = df["close"] / df["ma7"]
    df["close_to_ma20"] = df["close"] / df["ma20"]

    # how volatile was today
    df["daily_range"]   = (df["high"] - df["low"]) / df["close"]

    # did price open higher or lower than yesterday close
    df["gap"]           = (df["open"] - df["close"].shift(1)) / df["close"].shift(1)

    # target — next day's price change percentage
    df["target"]        = df["close"].shift(-1) / df["close"] - 1

    # drop rows with NaN from rolling calculations
    df = df.dropna()

    return df


if __name__ == "__main__":
    df = pd.read_csv("data/usable/NABIL.csv")
    df = add_features(df)
    print(f"Rows after feature engineering: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(df.tail(3))
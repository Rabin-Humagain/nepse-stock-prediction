import pandas as pd
import matplotlib.pyplot as plt
import os
os.makedirs("data/charts", exist_ok=True)
CLEANED_DIR = "data/cleaned"

def load_stock(symbol):
    filepath = f"{CLEANED_DIR}/{symbol}.csv"
    if not os.path.exists(filepath):
        print(f"{symbol} not found")
        return None
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df["date"])
    return df


def plot_price(symbol):
    df = load_stock(symbol)
    if df is None:
        return

    plt.figure(figsize=(14, 6))
    plt.plot(df["date"], df["close"], label="Close Price", color="blue", linewidth=1)
    plt.title(f"{symbol} — Close Price History")
    plt.xlabel("Date")
    plt.ylabel("Price (NPR)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"data/charts/{symbol}_price.png")
    plt.show()
    print(f"Chart saved for {symbol}")


def plot_with_moving_averages(symbol):
    df = load_stock(symbol)
    if df is None:
        return

    # calculate moving averages
    df["MA20"]  = df["close"].rolling(window=20).mean()   # 1 month trend
    df["MA50"]  = df["close"].rolling(window=50).mean()   # 2.5 month trend
    df["MA200"] = df["close"].rolling(window=200).mean()  # ~1 year trend

    plt.figure(figsize=(14, 6))
    plt.plot(df["date"], df["close"], label="Close Price", color="blue",   linewidth=1, alpha=0.6)
    plt.plot(df["date"], df["MA20"],  label="MA20",        color="orange", linewidth=1.5)
    plt.plot(df["date"], df["MA50"],  label="MA50",        color="green",  linewidth=1.5)
    plt.plot(df["date"], df["MA200"], label="MA200",       color="red",    linewidth=1.5)
    plt.title(f"{symbol} — Price with Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price (NPR)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    os.makedirs("data/charts", exist_ok=True)
    plt.savefig(f"data/charts/{symbol}_ma.png")
    plt.show()


def plot_volume(symbol):
    df = load_stock(symbol)
    if df is None:
        return

    plt.figure(figsize=(14, 4))
    plt.bar(df["date"], df["volume"], color="purple", alpha=0.5, label="Volume")
    plt.title(f"{symbol} — Trading Volume")
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.legend()
    plt.tight_layout()
    os.makedirs("data/charts", exist_ok=True)
    plt.savefig(f"data/charts/{symbol}_volume.png")
    plt.show()


def summary(symbol):
    df = load_stock(symbol)
    if df is None:
        return

    print(f"\n--- {symbol} Summary ---")
    print(f"Date range : {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"Total days : {len(df)}")
    print(f"Highest    : {df['close'].max()}")
    print(f"Lowest     : {df['close'].min()}")
    print(f"Current    : {df['close'].iloc[-1]}")
    change = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
    print(f"Total change: {change:.2f}% over entire period")


if __name__ == "__main__":
    # install matplotlib first if needed:
    # pip install matplotlib

    symbol = "NABIL"
    summary(symbol)
    plot_price(symbol)
    plot_with_moving_averages(symbol)
    #plot_volume(symbol)
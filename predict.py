import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from features import add_features
from datetime import date


def train_and_predict(symbol):
    filepath = f"data/usable/{symbol}.csv"
    if not os.path.exists(filepath):
        return None

    df = pd.read_csv(filepath)
    df = add_features(df)

    if len(df) < 100:
        return None

    feature_cols = [
        "price_change", "ma7", "ma20", "ma50",
        "close_to_ma7", "close_to_ma20",
        "daily_range", "gap"
    ]

    X = df[feature_cols]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)

    last_row = X.iloc[[-1]]
    tomorrow_change = model.predict(last_row)[0]
    current_price = df["close"].iloc[-1]
    predicted_price = current_price * (1 + tomorrow_change)

    return {
        "symbol": symbol,
        "current_price": round(current_price, 2),
        "predicted_change": round(tomorrow_change * 100, 2),
        "predicted_price": round(predicted_price, 2),
        "mae": round(mae, 4),
    }


def predict_all():
    usable_dir = "data/usable"
    files = os.listdir(usable_dir)

    results = []
    failed = 0

    print(f"Running predictions for {len(files)} companies...\n")

    for i, f in enumerate(files):
        symbol = f.replace(".csv", "")
        result = train_and_predict(symbol)
        if result:
            results.append(result)
        else:
            failed += 1

        if (i + 1) % 50 == 0:
            print(f"[{i+1}/{len(files)}] done...")

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("predicted_change", ascending=False)

    os.makedirs("data/predictions", exist_ok=True)
    output_path = f"data/predictions/{date.today()}.csv"
    results_df.to_csv(output_path, index=False)

    print(f"\n=== Top 10 Stocks to Watch Tomorrow ===")
    print(results_df.head(10).to_string(index=False))
    print(f"\n=== Bottom 5 Stocks to Avoid ===")
    print(results_df.tail(5).to_string(index=False))
    print(f"\nFailed: {failed}")
    print(f"Full results saved to {output_path}")


if __name__ == "__main__":
    predict_all()
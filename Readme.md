# NEPSE Stock Prediction

Automated stock price prediction system for Nepal Stock Exchange (NEPSE).

## What it does
- Scrapes daily price data for 325+ NEPSE listed companies
- Cleans and processes historical data (273,000+ rows)
- Trains a Random Forest model per company
- Predicts next day's price change
- Ranks all stocks by predicted gain daily

## Dataset
- 325 companies
- 273,574 rows
- Date range: 2021 → present
- Columns: date, open, high, low, close, symbol
- Source: sharesansar.com

## Project Structure
nepse-stock-prediction/
    data/
        usable/          ← clean historical data, 325 CSVs
        predictions/     ← daily prediction outputs
    get_symbols.py       ← scrape all company symbols
    get_history.py       ← scrape full price history
    daily_scraper.py     ← fetch today's prices
    clean.py             ← data cleaning pipeline
    filter_usable.py     ← filter companies with enough data
    features.py          ← feature engineering
    predict.py           ← Random Forest prediction model
    main.py              ← master pipeline, run this daily
    visualize.py         ← price charts and moving averages

## How to run
pip install -r requirements.txt
python main.py

## Sample Output
Top 10 Stocks to Watch Tomorrow:
NIL   — predicted +7.20%
NMIC  — predicted +6.70%
GMLI  — predicted +3.83%

## Built with
Python, pandas, scikit-learn, selenium, matplotlib, beautifulsoup4
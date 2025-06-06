import sys
import yfinance
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd  # Needed now since we reference pd.MultiIndex

def get_stock_data(ticker, start, end):
    df = yfinance.download(ticker, start=start, end=end, interval="1d")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)  # Keep just 'Close', 'Open', etc.
    return df

def main(args):

    if not args:
        print("Usage: python getinfo.py <ticker>")
        return

    ticker = args[0]
    end = datetime.today().strftime('%Y-%m-%d')
    start = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

    data = get_stock_data(ticker, start, end)
    data.reset_index(inplace=True)
    data["SMA_10"] = data["Close"].rolling(window=10).mean()
    data["SMA_20"] = data["Close"].rolling(window=20).mean()
    data["EMA_10"] = data["Close"].ewm(span=10, adjust=False).mean()
    data["EMA_20"] = data["Close"].ewm(span=20, adjust=False).mean()

    print(data.head())

    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=data, x="Date", y="Close", label=f"{ticker} Close Price")
    sns.lineplot(data=data, x="Date", y="SMA_10", label="10-day SMA")
    sns.lineplot(data=data, x="Date", y="SMA_20", label="20-day SMA")
    sns.lineplot(data=data, x="Date", y="EMA_10", label="10-day EMA", linestyle="--")
    sns.lineplot(data=data, x="Date", y="EMA_20", label="20-day EMA", linestyle="--")
    plt.title(f"{ticker} Daily Close Price ({start} to {end})")
    plt.xlabel("Date")
    plt.ylabel("Close Price (USD)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])

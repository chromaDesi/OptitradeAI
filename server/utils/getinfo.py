import sys
import yfinance
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd  # Needed now since we reference pd.MultiIndex
from tabulate import tabulate

#the main getter function for OLCHV, SMA, and EMA Data
def get_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    t = yfinance.Ticker(ticker=ticker)
    stock = yfinance.Ticker(ticker)
    data = stock.history(start=start, end=end)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)  # Keep just 'Close', 'Open', etc.
    data.reset_index(inplace=True)
    data["SMA_10"] = data["Close"].rolling(window=10).mean()
    data["SMA_20"] = data["Close"].rolling(window=20).mean()
    data["EMA_10"] = data["Close"].ewm(span=10, adjust=False).mean()
    data["EMA_20"] = data["Close"].ewm(span=20, adjust=False).mean()
    data.insert(0, "Symbol", ticker)
    return data

#for visualization purposes
def plot_stock_data(data: pd.DataFrame, ticker: str, start: str, end: str) -> None:
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
    

#meant for induvidual testing, otherwise not in use
def main(args) -> int:
    if not args:
        print("Usage: python getinfo.py <ticker>")
        return
    elif len(args) == 1:
        ticker = args[0]
        end = datetime.today().strftime('%Y-%m-%d')
        start = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    elif len(args) == 3:
        ticker = args[0]
        start = datetime.strptime(args[1], '%Y-%m-%d')
        end = datetime.strptime(args[2], '%Y-%m-%d')
    else:
        print("args needed: symbol_name , start_date, end_date")
    data = get_stock_data(ticker, start, end)
    print(f"Month : {start} to {end} for {ticker}")
    print(tabulate(data, headers='keys', tablefmt='psql'))
    if input("Wpuld you like to plot data (Y/N): ") == "Y":
        plot_stock_data(data, ticker, start, end)
    return 0
    

if __name__ == "__main__":
    main(sys.argv[1:])

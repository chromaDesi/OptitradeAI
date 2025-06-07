import pandas as pd
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import finnhub
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta
from tabulate import tabulate


#This method will scrape data from websites and socials about a given stock
def pull_text() -> np.ndarray:
    # Pull text from a file
    pass



#this method will be fed the text from the previous method and will return a sentiment score
def sentiment_analysis(text: str) -> dict:
    # Perform sentiment analysis on the text
    analyzer = SentimentIntensityAnalyzer()
    
    pass


def insider_sentiment(ticker, start, end):
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(dotenv_path=env_path)
    finnhub_client = finnhub_client = finnhub.Client(api_key=os.getenv("VITE_FINNHUB"))
    print(tabulate(pd.DataFrame(finnhub_client.stock_insider_sentiment(ticker, start, end)['data']), headers='keys', tablefmt='psql'))




def main():
    end = datetime.today().strftime('%Y-%m-%d')
    start = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    insider_sentiment("AAPL", start , end)
    
if __name__ == "__main__":
    main()
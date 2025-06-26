import pandas as pd
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import finnhub
from datetime import datetime, timedelta, date
from tabulate import tabulate
from mongo_aid import get_key
from transformers import pipeline
import requests
from bs4 import BeautifulSoup


def daterange(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(n)

def get_sentiment_news_daily_batched_finn(symbol: str, days: int = 30) -> pd.DataFrame:
    finnhub_client = finnhub_client = finnhub.Client(api_key=get_key("VITE_FINNHUB"))
    pipe = pipeline("text-classification", model="ProsusAI/finbert")

    start_date = date.today() - timedelta(days=days)
    end_date = date.today()

    results = {
        "date": [],
        "mean_sentiment": [],
        "std_sentiment": [],
        "article_count": []
    }

    for single_date in daterange(start_date, end_date):
        date_str = single_date.strftime('%Y-%m-%d')
        print(f"Fetching news for {symbol} on {date_str}")

        try:
            articles = finnhub_client.company_news(symbol, _from=date_str, to=date_str)
        except Exception as e:
            print(f"Error fetching articles for {date_str}: {e}")
            articles = []

        # Extract headline + summary
        texts = []
        for article in articles:
            headline = article.get("headline", "")
            summary = article.get("summary", "")
            if headline or summary:
                full_text = f"{headline} {summary}".strip()
                texts.append(full_text)

        if texts:
            try:
                outputs = pipe(texts, truncation=True)
                scores = []

                for i, (text, output) in enumerate(zip(texts, outputs)):
                    score = (
                        output["score"] if output["label"] == "positive"
                        else -output["score"] if output["label"] == "negative"
                        else 0
                    )
                    scores.append(score)

                    if i == 0:
                        print(f"\n📰 {date_str} Sample Article:")
                        print(f"Headline + Summary: {text[:300]}...")
                        print(f"Predicted Sentiment: {output['label']} ({score:.3f})\n")

                results["date"].append(single_date)
                results["mean_sentiment"].append(np.mean(scores))
                results["std_sentiment"].append(np.std(scores))
                results["article_count"].append(len(scores))

            except Exception as e:
                print(f"Sentiment error on {date_str}: {e}")
                results["date"].append(single_date)
                results["mean_sentiment"].append(np.nan)
                results["std_sentiment"].append(np.nan)
                results["article_count"].append(0)

        else:
            results["date"].append(single_date)
            results["mean_sentiment"].append(np.nan)
            results["std_sentiment"].append(np.nan)
            results["article_count"].append(0)

    df = pd.DataFrame(results)
    df.sort_values("date", inplace=True)
    return df

def get_sentiment_news_daily_batched_na(symbol: str, days: int = 30) -> pd.DataFrame:
    APIKEY = get_key("VITE_NEWSAPI")
    pipe = pipeline("text-classification", model="ProsusAI/finbert")

    start_date = date.today() - timedelta(days=days)
    end_date = date.today()

    results = {
        "date": [],
        "mean_sentiment": [],
        "std_sentiment": [],
        "article_count": []
    }

    query = symbol  # Simple keyword search; you can make this smarter if needed

    for single_date in daterange(start_date, end_date):
        date_str = single_date.strftime('%Y-%m-%d')
        print(f"Fetching news for {symbol} on {date_str}")

        url = (
            'https://newsapi.org/v2/everything?'
            f'q={query}&'
            f'from={date_str}&'
            f'to={date_str}&'
            'language=en&'  # ✅ English language filter
            'sortBy=publishedAt&'
            'pageSize=100&'
            f'apiKey={APIKEY}'
        )

        try:
            response = requests.get(url)
            response.raise_for_status()
            articles = response.json().get("articles", [])
        except Exception as e:
            print(f"Error fetching articles for {date_str}: {e}")
            articles = []

        # Build input text for sentiment model
        texts = []
        for article in articles:
            parts = []
            if article.get("title"):
                parts.append(article["title"])
            if article.get("description"):
                parts.append(article["description"])
            if article.get("content"):
                parts.append(article["content"])
            if parts:
                full_text = " ".join(parts)
                texts.append(full_text)

        if texts:
            try:
                outputs = pipe(texts, truncation=True)
                scores = []

                for i, (text, output) in enumerate(zip(texts, outputs)):
                    score = (
                        output["score"] if output["label"] == "positive"
                        else -output["score"] if output["label"] == "negative"
                        else 0
                    )
                    scores.append(score)

                    if i == 0:
                        print(f"\n📰 {date_str} Sample Article:")
                        print(f"Headline + Content: {text[:300]}...")
                        print(f"Predicted Sentiment: {output['label']} ({score:.3f})\n")

                results["date"].append(single_date)
                results["mean_sentiment"].append(np.mean(scores))
                results["std_sentiment"].append(np.std(scores))
                results["article_count"].append(len(scores))

            except Exception as e:
                print(f"Sentiment error on {date_str}: {e}")
                results["date"].append(single_date)
                results["mean_sentiment"].append(np.nan)
                results["std_sentiment"].append(np.nan)
                results["article_count"].append(0)

        else:
            results["date"].append(single_date)
            results["mean_sentiment"].append(np.nan)
            results["std_sentiment"].append(np.nan)
            results["article_count"].append(0)

    df = pd.DataFrame(results)
    df.sort_values("date", inplace=True)
    return df



def merge_daily_sentiment(finnhub_df: pd.DataFrame, newsapi_df: pd.DataFrame) -> pd.DataFrame:
    merged = pd.merge(
        finnhub_df,
        newsapi_df,
        on="date",
        suffixes=("_finnhub", "_newsapi")
    )

    # Compute a simple average of the two sources
    merged["mean_sentiment_avg"] = merged[
        ["mean_sentiment_finnhub", "mean_sentiment_newsapi"]
    ].mean(axis=1)

    # Optionally: compute average article count and std if needed
    merged["article_count_avg"] = merged[
        ["article_count_finnhub", "article_count_newsapi"]
    ].mean(axis=1)

    merged["std_sentiment_avg"] = merged[
        ["std_sentiment_finnhub", "std_sentiment_newsapi"]
    ].mean(axis=1)
    
    #Take the sentiment disagreement to flag potential market indecision
    merged["sentiment_disagreement"] = (
    merged["mean_sentiment_finnhub"] - merged["mean_sentiment_newsapi"]).abs()
    
    merged["sentiment_disagreement_pct"] = (
    merged["sentiment_disagreement"] / merged["std_sentiment_avg"]
    )

    return merged


#for long term trading, I would want to use news api, and for swing trades, use social media api

#This method will scrape data from websites and socials about a given stock
def pull_text(ticker: str) -> np.ndarray:
    response = requests.get(f"https://tradestie.com/apps/twitter/most-active-stocks/", headers = {"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        print(text)
    else:
        print(response.status_code)
        



#this method will be fed the text from the previous method and will return 
def get_sm_sentiement(text: str) -> dict:
    # Perform sentiment analysis on the text
    analyzer = SentimentIntensityAnalyzer()
    pass


def insider_sentiment(ticker, start, end):
    finnhub_client = finnhub_client = finnhub.Client(api_key=get_key("VITE_FINNHUB"))
    data = finnhub_client.stock_insider_sentiment(ticker, start, end)['data']
    print(tabulate(pd.DataFrame(data), headers='keys', tablefmt='psql'))


def get_insider_sentiment_score(ticker, start, end):
    client = finnhub.Client(api_key=get_key("VITE_FINNHUB"))
    data = client.stock_insider_sentiment(ticker, start, end)
    if not data:
        return 0  # Neutral if no activity

    df = pd.DataFrame(data)
    buy_sum = df[df['change'] > 0]['change'].sum()
    sell_sum = -df[df['change'] < 0]['change'].sum()
    
    if buy_sum + sell_sum == 0:
        return 0  # Avoid div by zero
    
    score = (buy_sum - sell_sum) / (buy_sum + sell_sum)  # normalized to -1..1
    return round(score, 3)


def main():
    '''end = datetime.today().strftime('%Y-%m-%d')
    start = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    #insider_sentiment("AAPL", start , end)
    df1 = get_sentiment_news_daily_batched_na("AMZN", days=10)
    df2 = get_sentiment_news_daily_batched_finn("AMZN", days=10)
    print(tabulate(df1, headers='keys', tablefmt='psql'))
    print(tabulate(df2, headers='keys', tablefmt='psql'))
    print(tabulate(merge_daily_sentiment(df2, df1), headers='keys', tablefmt='psql'))'''
    pull_text("AMZN")
    
    
if __name__ == "__main__":
    main()
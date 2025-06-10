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

'''
This file will contain all methods required to retrieve sentiment.
Both insider sentiment (MSPR) and News/Social sentiment will be extracted to be used in the model.
'''

def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)
        

def get_sentiment_news(ticker) -> str:
    # Initialize an empty list to collect scores (more efficient than np.append in loop)
    scores_list = []
    APIKEY = get_key("VITE_NEWS_API")
    
    # Initialize the sentiment analysis pipeline once
    pipe = pipeline("text-classification", model="ProsusAI/finbert")
    
    keyword = ticker
    
    # Iterate over the last year up until yesterday
    start_date = date.today() - timedelta(days=365)
    end_date = date.today() # Loop up to, but not including, today

    for single_date in daterange(start_date, end_date):
        newsurl = (
            'https://newsapi.org/v2/everything?'
            f'q={keyword}&'
            f'from={single_date.strftime('%Y-%m-%d')}&'
            'sortBy=popularity&' # Note: popularity might not be ideal for comprehensive sentiment. Consider 'relevancy' or 'publishedAt'.
            f'apiKey={APIKEY}'
        )
        
        try:
            response = requests.get(newsurl)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            
            articles = response.json()['articles']
            
            # Collects articles where keyword is found in either title or description
            filtered_articles = [
                article for article in articles 
                if article.get('title') and keyword.lower() in article['title'].lower() or 
                   article.get('description') and keyword.lower() in article['description'].lower()
            ]
            
            # Sentiment analysis on each article
            for article in filtered_articles:
                if article.get('content'): # Ensure 'content' key exists and is not None
                    sentiment = pipe(article['content'])[0]
                    scores_list.append(sentiment['score'])
                else:
                    print(f"Warning: Article with no content for {single_date} - {article.get('title', 'N/A')}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news for {single_date}: {e}")
        except KeyError as e:
            print(f"Error parsing JSON for {single_date} (missing key): {e}")
        except IndexError: # Happens if pipe() returns an empty list, though unlikely for finbert
            print(f"Warning: Could not get sentiment for an article on {single_date}")

    if scores_list:
        arr = np.array(scores_list) # Convert list to numpy array at the end
        print(f'Overall yearly sentiment for {ticker} is {np.mean(arr)}')
    else:
        print(f'No sentiment data found for {ticker} in the last year.')


#for long term trading, I would want to use news api, and for swing trades, use social media api

#This method will scrape data from websites and socials about a given stock
def pull_text() -> np.ndarray:
    # Pull text from a file
    pass



#this method will be fed the text from the previous method and will return 
def get_sm_sentiement(text: str) -> dict:
    # Perform sentiment analysis on the text
    analyzer = SentimentIntensityAnalyzer()
    pass


def insider_sentiment(ticker, start, end):
    finnhub_client = finnhub_client = finnhub.Client(api_key=get_key("VITE_FINNHUB"))
    data = finnhub_client.stock_insider_sentiment(ticker, start, end)['data']
    print(tabulate(pd.DataFrame(data), headers='keys', tablefmt='psql'))


def main():
    end = datetime.today().strftime('%Y-%m-%d')
    start = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    insider_sentiment("AAPL", start , end)
    
if __name__ == "__main__":
    main()
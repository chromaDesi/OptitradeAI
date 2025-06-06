import os
from dotenv import load_dotenv
from pymongo import MongoClient
from getinfo import get_stock_data
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd

# Load .env
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

# MongoDB setup
dbclient = MongoClient(os.getenv("MONGO_URL"))
db = dbclient["OptitradeAI"]
collection = db["stock_prices"]

# Get data
end = datetime.today().strftime('%Y-%m-%d')
start = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
ticker = input("Enter your desired stock symbol: ")
df = get_stock_data(ticker, start, end)

for _, row in df.iterrows():
    query = {"Symbol": row["Symbol"], "Date": row["Date"].strftime('%Y-%m-%d')}
    
    # Only insert if not already present
    if not collection.find_one(query):
        collection.insert_one(row.to_dict())


# Upsert each row to prevent duplicates


print("Complete")

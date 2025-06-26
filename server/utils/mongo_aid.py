import os
from dotenv import load_dotenv
from pymongo import MongoClient
from getinfo import get_stock_data
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
from tabulate import tabulate

#used to retrieve a key located in .env
def get_key(keyname: str) -> (str | None):
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(dotenv_path=env_path)
    return os.getenv(keyname)
    
#used to establish connection with MongoDB   
def setup(collection_name: str):
        dbclient = MongoClient(get_key("MONGO_URL"))
        db = dbclient["OptitradeAI"]
        collection = db[collection_name]
        return collection

#add stock data to MongoDB
def add_stock_data_to_db(ticker:str, start:str = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d'), end: str = datetime.today().strftime('%Y-%m-%d')) -> int:
    try:
        #load collection
        collection = setup("stock_prices")
        # Get data
        df = get_stock_data(ticker, start, end)

        for _, row in df.iterrows():
            query = {"Symbol": row["Symbol"], "Date": row["Date"].strftime('%Y-%m-%d')}
            
            # Only insert if not already present
            if not collection.find_one(query):
                collection.insert_one(row.to_dict())
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1

#Retrieve documents from collections located in the database
def retrieve_stock_data_from_db(ticker: str, start_date: str, end_date:str) -> pd.DataFrame:
    try:
        #load collection
        collection = setup("stock_prices")
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        docs = list(collection.find({"Symbol": ticker, "Date": {"$gte": start_dt, "$lte": end_dt}}))
        df = pd.DataFrame(docs)
        if df.empty:
            print("Data not in database, importing right now:")
            add_stock_data_to_db(ticker, start_date, end_date)
            return retrieve_stock_data_from_db(ticker, start_date, end_date)
        if "_id" in df.columns:
            df.drop(columns=["_id"], inplace=True)
        print(tabulate(df, headers='keys', tablefmt='psql'))
        return df
    except Exception as e:
        print(f"Error: {e}")

#Only used for testing, No inteded Use 
def main():
    while True:
        choice = int(input("Menu:\n1. Add data\n2. Retrieve data\n3. Exit\nChoose: "))
        match choice:
            case 1:
                add_stock_data_to_db(input("Enter your desired stock symbol: ").strip())
            case 2:
                ticker = input("Enter your desired stock symbol: ").strip()
                start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter the end date (YYYY-MM-DD): ").strip()
                retrieve_stock_data_from_db(ticker, start_date, end_date)
            case 3:
                return
if __name__ == "__main__":
    main()
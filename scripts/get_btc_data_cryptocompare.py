import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY")

def fetch_btc_daily_prices(limit, to_timestamp):
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        "fsym": "BTC",
        "tsym": "USD",
        "limit": limit,
        "toTs": to_timestamp,
        "api_key": API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()["Data"]["Data"]
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.rename(columns={"time": "date"}, inplace=True)
    return df

def save_btc_period(start_date_str, end_date_str, filename):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    limit = (end_date - start_date).days
    to_timestamp = int(end_date.timestamp())
    df = fetch_btc_daily_prices(limit, to_timestamp)
    # Filter exactly to date range
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    df.to_csv(f"../data/{filename}.csv", index=False)
    print(f"{filename}.csv saved.")

if __name__ == "__main__":
    save_btc_period("2024-08-20", "2024-09-20", "btc_control_period")
    save_btc_period("2024-10-20", "2024-11-20", "btc_event_period")
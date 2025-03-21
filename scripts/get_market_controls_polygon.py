import requests
import pandas as pd
import time
from datetime import datetime
from dotenv import load_dotenv
import os

# Load Polygon.io API key from .env
load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")

def fetch_polygon_timeseries(ticker, start_date, end_date, output_file):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": "5000",
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'results' not in data:
            print(f"Error: No data returned for {ticker}. Response: {data}")
            return

        df = pd.DataFrame(data['results'])
        df['date'] = pd.to_datetime(df['t'], unit='ms')
        df.rename(columns={
            'o': 'open',
            'h': 'high',
            'l': 'low',
            'c': 'close',
            'v': 'volume'
        }, inplace=True)

        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        df.to_csv(f"../data/{output_file}.csv", index=False)
        print(f" {output_file}.csv saved.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {ticker}: {e}")

if __name__ == "__main__":
    # Correct year data (2024)
    fetch_polygon_timeseries("SPY", "2024-08-20", "2024-09-20", "sp500_control_period")
    fetch_polygon_timeseries("SPY", "2024-10-20", "2024-11-20", "sp500_event_period")

    fetch_polygon_timeseries("VXX", "2024-08-20", "2024-09-20", "vix_control_period")
    fetch_polygon_timeseries("VXX", "2024-10-20", "2024-11-20", "vix_event_period")

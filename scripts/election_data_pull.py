import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
CRYPTOCOMPARE_API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")

# Pull BTC Data
def fetch_btc_daily_prices(limit, to_timestamp):
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        "fsym": "BTC",
        "tsym": "USD",
        "limit": limit,
        "toTs": to_timestamp,
        "api_key": CRYPTOCOMPARE_API_KEY
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
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    df.to_csv(f"data/{filename}.csv", index=False)
    print(f"{filename}.csv saved.")

# Pull SP500 & VIX Data
def fetch_polygon_timeseries(ticker, start_date, end_date, output_file):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": "5000",
        "apiKey": POLYGON_API_KEY
    }

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
    df.to_csv(f"data/{output_file}.csv", index=False)
    print(f"{output_file}.csv saved.")

# Pull Treasury Yields
def fetch_fred_data(series_id, start_date, end_date, output_file):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if 'observations' not in data:
        print(f"Error: No data returned for {series_id}. Response: {data}")
        return

    df = pd.DataFrame(data['observations'])
    df.rename(columns={"date": "date", "value": "yield"}, inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['yield'] = pd.to_numeric(df['yield'], errors='coerce')
    df.dropna(subset=['yield'], inplace=True)
    df.to_csv(f"data/{output_file}.csv", index=False)
    print(f"{output_file}.csv saved.")

if __name__ == "__main__":
    save_btc_period("2024-08-20", "2024-09-20", "btc_control_period")
    save_btc_period("2024-10-20", "2024-11-20", "btc_event_period")

    fetch_polygon_timeseries("SPY", "2024-08-20", "2024-09-20", "sp500_control_period")
    fetch_polygon_timeseries("SPY", "2024-10-20", "2024-11-20", "sp500_event_period")

    fetch_polygon_timeseries("VXX", "2024-08-20", "2024-09-20", "vix_control_period")
    fetch_polygon_timeseries("VXX", "2024-10-20", "2024-11-20", "vix_event_period")

    fetch_fred_data("DGS10", "2024-08-20", "2024-09-20", "treasury_yield_control_period")
    fetch_fred_data("DGS10", "2024-10-20", "2024-11-20", "treasury_yield_event_period")

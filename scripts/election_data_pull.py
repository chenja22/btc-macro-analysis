import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
CRYPTO_API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY")
POLYGON_KEY = os.getenv("POLYGON_API_KEY")
FRED_KEY = os.getenv("FRED_API_KEY")

def get_btc_data(days, end_ts):
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        "fsym": "BTC",
        "tsym": "USD",
        "limit": days,
        "toTs": end_ts,
        "api_key": CRYPTO_API_KEY
    }
    r = requests.get(url, params=params)
    data = r.json()["Data"]["Data"]
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.rename(columns={"time": "date"}, inplace=True)
    return df

def save_btc(start, end, name):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    days = (end_date - start_date).days
    end_ts = int(end_date.timestamp())
    df = get_btc_data(days, end_ts)
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    df.to_csv(f"data/{name}.csv", index=False)

def get_stock_data(ticker, start, end, name):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": "5000",
        "apiKey": POLYGON_KEY
    }
    r = requests.get(url, params=params)
    data = r.json()
    if 'results' not in data:
        print(f"No data for {ticker}")
        return
    df = pd.DataFrame(data['results'])
    df['date'] = pd.to_datetime(df['t'], unit='ms')
    df.rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'}, inplace=True)
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df.to_csv(f"data/{name}.csv", index=False)

def get_treasury_data(series, start, end, name):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series,
        "api_key": FRED_KEY,
        "file_type": "json",
        "observation_start": start,
        "observation_end": end
    }
    r = requests.get(url, params=params)
    data = r.json()
    if 'observations' not in data:
        print(f"No data for {series}")
        return
    df = pd.DataFrame(data['observations'])
    df.rename(columns={"value": "yield"}, inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['yield'] = pd.to_numeric(df['yield'], errors='coerce')
    df.dropna(subset=['yield'], inplace=True)
    df.to_csv(f"data/{name}.csv", index=False)

if __name__ == "__main__":
    save_btc("2024-08-20", "2024-09-20", "btc_control")
    save_btc("2024-10-20", "2024-11-20", "btc_event")

    get_stock_data("SPY", "2024-08-20", "2024-09-20", "sp500_control")
    get_stock_data("SPY", "2024-10-20", "2024-11-20", "sp500_event")

    get_stock_data("VXX", "2024-08-20", "2024-09-20", "vix_control")
    get_stock_data("VXX", "2024-10-20", "2024-11-20", "vix_event")

    get_treasury_data("DGS10", "2024-08-20", "2024-09-20", "treasury_control")
    get_treasury_data("DGS10", "2024-10-20", "2024-11-20", "treasury_event")

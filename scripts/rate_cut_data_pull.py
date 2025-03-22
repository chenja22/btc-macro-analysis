import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
CRYPTO_KEY = os.getenv("CRYPTOCOMPARE_API_KEY")
POLYGON_KEY = os.getenv("POLYGON_API_KEY")
FRED_KEY = os.getenv("FRED_API_KEY")

def make_data_dir():
    path = os.path.join(os.path.dirname(__file__), '../data/raw_data')
    os.makedirs(path, exist_ok=True)
    return path

def get_btc_data(days, end_ts):
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        "fsym": "BTC",
        "tsym": "USD",
        "limit": days,
        "toTs": end_ts,
        "api_key": CRYPTO_KEY
    }
    r = requests.get(url, params=params)
    data = r.json()["Data"]["Data"]
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.rename(columns={"time": "date"}, inplace=True)
    return df

def save_btc(start, end, name):
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    days = (end_dt - start_dt).days
    end_ts = int(end_dt.timestamp())
    df = get_btc_data(days, end_ts)
    df = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]
    out_dir = make_data_dir()
    df.to_csv(os.path.join(out_dir, f"{name}.csv"), index=False)

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
    out_dir = make_data_dir()
    df.to_csv(os.path.join(out_dir, f"{name}.csv"), index=False)

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
    out_dir = make_data_dir()
    df.to_csv(os.path.join(out_dir, f"{name}.csv"), index=False)

if __name__ == "__main__":
    save_btc("2025-01-15", "2025-02-15", "btc_event")
    save_btc("2024-12-15", "2025-01-14", "btc_control")

    get_stock_data("SPY", "2025-01-15", "2025-02-15", "sp500_event")
    get_stock_data("SPY", "2024-12-15", "2025-01-14", "sp500_control")

    get_stock_data("VXX", "2025-01-15", "2025-02-15", "vix_event")
    get_stock_data("VXX", "2024-12-15", "2025-01-14", "vix_control")

    get_treasury_data("DGS10", "2025-01-15", "2025-02-15", "treasury_event")
    get_treasury_data("DGS10", "2024-12-15", "2025-01-14", "treasury_control")

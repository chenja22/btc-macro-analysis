import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
CRYPTOCOMPARE_API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")


def ensure_output_dir():
    output_dir = os.path.join(os.path.dirname(__file__), '../data/raw_data')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

# Pull BTC data
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
    output_dir = ensure_output_dir()
    df.to_csv(os.path.join(output_dir, f"{filename}.csv"), index=False)

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

    df = pd.DataFrame(data['results'])
    df['date'] = pd.to_datetime(df['t'], unit='ms')
    df.rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'}, inplace=True)
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    output_dir = ensure_output_dir()
    df.to_csv(os.path.join(output_dir, f"{output_file}.csv"), index=False)

# Pull Treasury yields
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

    df = pd.DataFrame(data['observations'])
    df.rename(columns={"date": "date", "value": "yield"}, inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['yield'] = pd.to_numeric(df['yield'], errors='coerce')
    df.dropna(subset=['yield'], inplace=True)
    output_dir = ensure_output_dir()
    df.to_csv(os.path.join(output_dir, f"{output_file}.csv"), index=False)

if __name__ == "__main__":
    # BTC Data for Interest Rate Event
    save_btc_period("2025-01-15", "2025-02-15", "btc_interest_rate_event_period")
    save_btc_period("2024-12-15", "2025-01-14", "btc_interest_rate_control_period")

    # SP500 & VIX Data
    fetch_polygon_timeseries("SPY", "2025-01-15", "2025-02-15", "sp500_interest_rate_event_period")
    fetch_polygon_timeseries("SPY", "2024-12-15", "2025-01-14", "sp500_interest_rate_control_period")

    fetch_polygon_timeseries("VXX", "2025-01-15", "2025-02-15", "vix_interest_rate_event_period")
    fetch_polygon_timeseries("VXX", "2024-12-15", "2025-01-14", "vix_interest_rate_control_period")

    # Treasury yield Data
    fetch_fred_data("DGS10", "2025-01-15", "2025-02-15", "treasury_yield_interest_rate_event_period")
    fetch_fred_data("DGS10", "2024-12-15", "2025-01-14", "treasury_yield_interest_rate_control_period")

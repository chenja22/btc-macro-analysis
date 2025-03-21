import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load FRED API key from .env
load_dotenv()
API_KEY = os.getenv("FRED_API_KEY")

def fetch_fred_data(series_id, start_date, end_date, output_file):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'observations' not in data or len(data['observations']) == 0:
            print(f"Error: No data returned for {series_id}. Response: {data}")
            return

        df = pd.DataFrame(data['observations'])
        df.rename(columns={"date": "date", "value": "yield"}, inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        df['yield'] = pd.to_numeric(df['yield'], errors='coerce')
        df.dropna(subset=['yield'], inplace=True)
        df.to_csv(f"../data/{output_file}.csv", index=False)
        print(f"✅ {output_file}.csv saved.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {series_id}: {e}")

if __name__ == "__main__":
# 10-Year Treasury Constant Maturity Rate (series_id: DGS10)
    fetch_fred_data("DGS10", "2024-08-20", "2024-09-20", "treasury_yield_control_period")
    fetch_fred_data("DGS10", "2024-10-20", "2024-11-20", "treasury_yield_event_period")

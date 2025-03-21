import pandas as pd
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def clean_btc_data(filename):
    filepath = os.path.join(base_dir, filename)
    df = pd.read_csv(filepath, parse_dates=['date'])
    df = df[['date', 'open', 'high', 'low', 'close', 'volumeto']]
    df.rename(columns={'volumeto': 'volume'}, inplace=True)
    df.dropna(inplace=True)
    df.sort_values('date', inplace=True)
    df.to_csv(filepath.replace('.csv', '_clean.csv'), index=False)
    print(f"Cleaned {filename} and saved.")

def clean_market_data(filename):
    filepath = os.path.join(base_dir, filename)
    df = pd.read_csv(filepath, parse_dates=['date'])
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df.dropna(inplace=True)
    df.sort_values('date', inplace=True)
    df.to_csv(filepath.replace('.csv', '_clean.csv'), index=False)
    print(f"Cleaned {filename} and saved.")

def clean_treasury_data(filename):
    filepath = os.path.join(base_dir, filename)
    df = pd.read_csv(filepath, parse_dates=['date'])
    df.rename(columns={'yield': 'treasury_yield'}, inplace=True)
    df = df[['date', 'treasury_yield']]
    df.dropna(inplace=True)
    df.sort_values('date', inplace=True)
    df.to_csv(filepath.replace('.csv', '_clean.csv'), index=False)
    print(f"Cleaned {filename} and saved.")

if __name__ == "__main__":
    clean_btc_data("btc_control_period.csv")
    clean_btc_data("btc_event_period.csv")
    clean_market_data("sp500_control_period.csv")
    clean_market_data("sp500_event_period.csv")
    clean_market_data("vix_control_period.csv")
    clean_market_data("vix_event_period.csv")
    clean_treasury_data("treasury_yield_control_period.csv")
    clean_treasury_data("treasury_yield_event_period.csv")

import pandas as pd
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def clean_btc_data(filename):
    path = os.path.join(base_dir, filename)
    data = pd.read_csv(path, parse_dates=['date'])
    data = data[['date', 'open', 'high', 'low', 'close', 'volumeto']]
    data.rename(columns={'volumeto': 'volume'}, inplace=True)
    data.dropna(inplace=True)
    data.sort_values('date', inplace=True)
    cleaned_path = path.replace('.csv', '_clean.csv')
    data.to_csv(cleaned_path, index=False)
    print(f"{filename} cleaned and saved as {os.path.basename(cleaned_path)}")

def clean_market_data(filename):
    path = os.path.join(base_dir, filename)
    data = pd.read_csv(path, parse_dates=['date'])
    data = data[['date', 'open', 'high', 'low', 'close', 'volume']]
    data.dropna(inplace=True)
    data.sort_values('date', inplace=True)
    cleaned_path = path.replace('.csv', '_clean.csv')
    data.to_csv(cleaned_path, index=False)
    print(f"{filename} cleaned and saved as {os.path.basename(cleaned_path)}")

def clean_treasury_data(filename):
    path = os.path.join(base_dir, filename)
    data = pd.read_csv(path, parse_dates=['date'])
    data.rename(columns={'yield': 'treasury_yield'}, inplace=True)
    data = data[['date', 'treasury_yield']]
    data.dropna(inplace=True)
    data.sort_values('date', inplace=True)
    cleaned_path = path.replace('.csv', '_clean.csv')
    data.to_csv(cleaned_path, index=False)
    print(f"{filename} cleaned and saved as {os.path.basename(cleaned_path)}")

if __name__ == "__main__":
    clean_btc_data("btc_control_period.csv")
    clean_btc_data("btc_event_period.csv")
    clean_market_data("sp500_control_period.csv")
    clean_market_data("sp500_event_period.csv")
    clean_market_data("vix_control_period.csv")
    clean_market_data("vix_event_period.csv")
    clean_treasury_data("treasury_yield_control_period.csv")
    clean_treasury_data("treasury_yield_event_period.csv")

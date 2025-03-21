import pandas as pd

def clean_btc_data(filepath):
    df = pd.read_csv(filepath, parse_dates=['date'])
    df = df[['date', 'open', 'high', 'low', 'close', 'volumefrom']]
    df.rename(columns={'volumefrom': 'volume'}, inplace=True)
    df.dropna(inplace=True)
    df.sort_values('date', inplace=True)
    df.to_csv(filepath.replace('.csv', '_clean.csv'), index=False)

def clean_market_data(filepath):
    df = pd.read_csv(filepath, parse_dates=['date'])
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df.dropna(inplace=True)
    df.sort_values('date', inplace=True)
    df.to_csv(filepath.replace('.csv', '_clean.csv'), index=False)

def clean_treasury_data(filepath):
    df = pd.read_csv(filepath, parse_dates=['date'])
    df.rename(columns={'yield': 'treasury_yield'}, inplace=True)
    df = df[['date', 'treasury_yield']]
    df.dropna(inplace=True)
    df.sort_values('date', inplace=True)
    df.to_csv(filepath.replace('.csv', '_clean.csv'), index=False)

if __name__ == "__main__":
    clean_btc_data("data/raw_data/btc_interest_rate_control_period.csv")
    clean_btc_data("data/raw_data/btc_interest_rate_event_period.csv")

    clean_market_data("data/raw_data/sp500_interest_rate_control_period.csv")
    clean_market_data("data/raw_data/sp500_interest_rate_event_period.csv")

    clean_market_data("data/raw_data/vix_interest_rate_control_period.csv")
    clean_market_data("data/raw_data/vix_interest_rate_event_period.csv")

    clean_treasury_data("data/raw_data/treasury_yield_interest_rate_control_period.csv")
    clean_treasury_data("data/raw_data/treasury_yield_interest_rate_event_period.csv")

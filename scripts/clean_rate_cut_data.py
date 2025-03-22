import pandas as pd

def clean_btc(file):
    data = pd.read_csv(file, parse_dates=['date'])
    data = data[['date', 'open', 'high', 'low', 'close', 'volumefrom']]
    data.rename(columns={'volumefrom': 'volume'}, inplace=True)
    data.dropna(inplace=True)
    data.sort_values('date', inplace=True)
    data.to_csv(file.replace('.csv', '_clean.csv'), index=False)
    print(f"Cleaned {file}")

def clean_market(file):
    data = pd.read_csv(file, parse_dates=['date'])
    data = data[['date', 'open', 'high', 'low', 'close', 'volume']]
    data.dropna(inplace=True)
    data.sort_values('date', inplace=True)
    data.to_csv(file.replace('.csv', '_clean.csv'), index=False)
    print(f"Cleaned {file}")

def clean_treasury(file):
    data = pd.read_csv(file, parse_dates=['date'])
    data.rename(columns={'yield': 'treasury_yield'}, inplace=True)
    data = data[['date', 'treasury_yield']]
    data.dropna(inplace=True)
    data.sort_values('date', inplace=True)
    data.to_csv(file.replace('.csv', '_clean.csv'), index=False)
    print(f"Cleaned {file}")

if __name__ == "__main__":
    clean_btc("data/raw_data/btc_interest_rate_control_period.csv")
    clean_btc("data/raw_data/btc_interest_rate_event_period.csv")
    clean_market("data/raw_data/sp500_interest_rate_control_period.csv")
    clean_market("data/raw_data/sp500_interest_rate_event_period.csv")
    clean_market("data/raw_data/vix_interest_rate_control_period.csv")
    clean_market("data/raw_data/vix_interest_rate_event_period.csv")
    clean_treasury("data/raw_data/treasury_yield_interest_rate_control_period.csv")
    clean_treasury("data/raw_data/treasury_yield_interest_rate_event_period.csv")

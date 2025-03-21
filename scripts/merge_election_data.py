import pandas as pd
import numpy as np

# Load BTC Data
btc_control = pd.read_csv("data/btc_control_period_clean.csv", parse_dates=["date"])
btc_event = pd.read_csv("data/btc_event_period_clean.csv", parse_dates=["date"])

btc_control['log_return'] = np.log(btc_control['close'] / btc_control['close'].shift(1))
btc_event['log_return'] = np.log(btc_event['close'] / btc_event['close'].shift(1))

btc_all = pd.concat([btc_control, btc_event])
btc_all['event_period'] = btc_all['date'].apply(lambda d: 1 if d in btc_event['date'].values else 0)

# Load SP500 and VIX data
sp500_all = pd.concat([
    pd.read_csv("data/sp500_control_period_clean.csv", parse_dates=["date"]),
    pd.read_csv("data/sp500_event_period_clean.csv", parse_dates=["date"])
])
sp500_all.rename(columns={"close": "sp500_close"}, inplace=True)
sp500_all['sp500_return'] = sp500_all['sp500_close'].pct_change()

vix_all = pd.concat([
    pd.read_csv("data/vix_control_period_clean.csv", parse_dates=["date"]),
    pd.read_csv("data/vix_event_period_clean.csv", parse_dates=["date"])
])
vix_all.rename(columns={"close": "vix_close"}, inplace=True)
vix_all['vix_change'] = vix_all['vix_close'].pct_change()

# Load Treasury yield data
treasury_all = pd.concat([
    pd.read_csv("data/treasury_yield_control_period_clean.csv", parse_dates=["date"]),
    pd.read_csv("data/treasury_yield_event_period_clean.csv", parse_dates=["date"])
])
treasury_all['yield_change'] = treasury_all['treasury_yield'].diff()

# Merge data
btc_all = pd.merge_asof(
    btc_all.sort_values('date'),
    sp500_all[['date', 'sp500_return']].sort_values('date'),
    on='date',
    direction='backward'
)
btc_all = pd.merge_asof(
    btc_all.sort_values('date'),
    vix_all[['date', 'vix_change']].sort_values('date'),
    on='date',
    direction='backward'
)
btc_all = pd.merge_asof(
    btc_all.sort_values('date'),
    treasury_all[['date', 'yield_change']].sort_values('date'),
    on='date',
    direction='backward'
)

btc_all.dropna(subset=['log_return', 'sp500_return', 'vix_change', 'yield_change'], inplace=True)

# Save merged CSV
btc_all.to_csv("data/btc_all_merged_clean.csv", index=False)

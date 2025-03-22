import pandas as pd
import numpy as np

btc_ctrl = pd.read_csv("data/btc_control_period_clean.csv", parse_dates=["date"])
btc_evt = pd.read_csv("data/btc_event_period_clean.csv", parse_dates=["date"])

btc_ctrl['log_ret'] = np.log(btc_ctrl['close'] / btc_ctrl['close'].shift(1))
btc_evt['log_ret'] = np.log(btc_evt['close'] / btc_evt['close'].shift(1))

btc = pd.concat([btc_ctrl, btc_evt])
btc['event'] = btc['date'].apply(lambda x: 1 if x in btc_evt['date'].values else 0)

sp500 = pd.concat([
    pd.read_csv("data/sp500_control_period_clean.csv", parse_dates=["date"]),
    pd.read_csv("data/sp500_event_period_clean.csv", parse_dates=["date"])
])
sp500.rename(columns={"close": "sp500_close"}, inplace=True)
sp500['sp500_ret'] = sp500['sp500_close'].pct_change()

vix = pd.concat([
    pd.read_csv("data/vix_control_period_clean.csv", parse_dates=["date"]),
    pd.read_csv("data/vix_event_period_clean.csv", parse_dates=["date"])
])
vix.rename(columns={"close": "vix_close"}, inplace=True)
vix['vix_change'] = vix['vix_close'].pct_change()

treasury = pd.concat([
    pd.read_csv("data/treasury_yield_control_period_clean.csv", parse_dates=["date"]),
    pd.read_csv("data/treasury_yield_event_period_clean.csv", parse_dates=["date"])
])
treasury['yield_diff'] = treasury['treasury_yield'].diff()

btc = pd.merge_asof(btc.sort_values('date'), sp500[['date', 'sp500_ret']].sort_values('date'), on='date', direction='backward')
btc = pd.merge_asof(btc.sort_values('date'), vix[['date', 'vix_change']].sort_values('date'), on='date', direction='backward')
btc = pd.merge_asof(btc.sort_values('date'), treasury[['date', 'yield_diff']].sort_values('date'), on='date', direction='backward')

btc.dropna(subset=['log_ret', 'sp500_ret', 'vix_change', 'yield_diff'], inplace=True)

btc.to_csv("data/btc_all_merged_clean.csv", index=False)

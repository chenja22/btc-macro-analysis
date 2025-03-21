import pandas as pd

# Clean SP500 dates
sp500_df = pd.read_csv("../data/sp500_control_period.csv")
sp500_df['date'] = sp500_df['date'].str.slice(0, 10)
sp500_df.to_csv("../data/sp500_control_period_clean.csv", index=False)
print("SP500 control period cleaned and saved.")

# Clean VIX dates
vix_df = pd.read_csv("../data/vix_control_period.csv")
vix_df['date'] = vix_df['date'].str.slice(0, 10)
vix_df.to_csv("../data/vix_control_period_clean.csv", index=False)
print("VIX control period cleaned and saved.")

# Clean Treasury yield data
treasury_yield = pd.read_csv("../data/treasury_yield_control_period.csv", usecols=['date', 'yield'])
treasury_yield.rename(columns={'yield': 'treasury_yield'}, inplace=True)
treasury_yield.to_csv("../data/treasury_yield_control_period_clean.csv", index=False)
print("Treasury yield control period cleaned and saved.")
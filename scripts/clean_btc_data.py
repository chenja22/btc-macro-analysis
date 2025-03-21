import pandas as pd

def clean_and_save(filepath, output_filename):
    df = pd.read_csv(filepath)
    df = df[["date", "open", "high", "low", "close", "volumeto"]]
    df.rename(columns={"volumeto": "volume"}, inplace=True)
    df.to_csv(f"../data/{output_filename}.csv", index=False)
    print(f"Cleaned {output_filename}.csv saved.")

if __name__ == "__main__":
    clean_and_save("../data/btc_control_period.csv", "btc_control_period_clean")
    clean_and_save("../data/btc_event_period.csv", "btc_event_period_clean")

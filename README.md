This project studies how Bitcoin’s price and volatility respond to major macroeconomic events using an event study methodology. The two key events analyzed are the 2024 U.S. Presidential Election and the Federal Reserve’s interest rate cut in early 2025. The research employs statistical modeling and visualization in Python.

## Methodology
Bitcoin price data is collected using the CoinGecko API, from which daily log returns and realized volatility are computed. The following outcome variables are evaluated:
- Average daily return
- Return volatility
- Maximum drawdown

Each event window is compared against a control period without macroeconomic shocks. Control variables may include S&P 500 returns, VIX, and 10-year U.S. Treasury yields.

A Difference-in-Differences (DiD) regression framework is employed with the following specification:
```
yt = α + β1 * EventPeriodt + β2 * MarketControlst + ϵt
```
A GARCH(1,1) model may also be used to assess volatility dynamics.

## Folder Structure
- `data/` — stores CSV data files
- `scripts/` — data collection scripts using CoinGecko API
- `notebooks/` — includes `analysis.ipynb`

## Technologies
- Python (pandas, numpy, matplotlib, seaborn, statsmodels, arch, requests)
- Jupyter Notebooks

## Reproduction
1. Clone this repository.
2. Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Add your CoinGecko API key in `get_btc_data_coingecko.py`
5. Run scripts from `scripts/` to pull data.
6. Open and run `notebooks/analysis.ipynb` to perform the analysis.
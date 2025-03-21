# Bitcoin Price and Volatility Response to Macroeconomic Events

This project analyzes how Bitcoin’s price and volatility react to major macroeconomic events using an event study framework. The focus is on two key events: the 2024 U.S. Presidential Election and the Federal Reserve’s interest rate cut in early 2025. The analysis is conducted in Python and includes statistical modeling, visualizations, and comparisons to stable control periods.

## Overview of Methodology
Daily Bitcoin price data is collected via the CoinGecko API, from which log returns and realized volatility are calculated. The study focuses on three main outcome measures:
- Average daily return
- Return volatility
- Maximum drawdown

Each event window is compared to a control window without significant macroeconomic activity. In addition to Bitcoin data, the analysis incorporates control variables such as S&P 500 returns, VIX changes, and 10-year U.S. Treasury yield changes.

A Difference-in-Differences (DiD) regression is used to test for significant changes in Bitcoin returns and volatility during the event windows. The model takes the following form:

yt = α + β1 * EventPeriodt + β2 * MarketControlst + ϵt

## Tools and Libraries
- Python (pandas, numpy, matplotlib, seaborn, statsmodels, arch, requests)
- Jupyter Notebooks


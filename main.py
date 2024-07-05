# Test script for financial data fetchers
from datetime import datetime

from src.financialPlotter import FinancialPlotter
from src.securityDataFetcher import (
    AlphaVantageDataFetcher,
    YahooFinanceDataFetcher,
)

alpha_vantage_key = 'Your-API-Key'
yahoo_fetcher = YahooFinanceDataFetcher()
alpha_vantage_fetcher = AlphaVantageDataFetcher(alpha_vantage_key)

# Define tickers and date range for testing
ticker = 'AAPL'  # Yahoo and Alpha Vantage use simple tickers
start_date = '2024-01-01'
end_date = '2024-06-01'

# Fetch historical data using Yahoo Finance and Alpha Vantage
print("Fetching data from Yahoo Finance...")
df_yahoo = yahoo_fetcher.fetch_data(ticker, start_date, end_date)
print(df_yahoo.tail())

print("\nFetching data from Alpha Vantage...")
df_alpha_vantage = alpha_vantage_fetcher.fetch_data(ticker, start_date,
                                                    end_date)
print(df_alpha_vantage.head())

# Fetch and print fundamentals from Yahoo Finance and Alpha Vantage
# print("\nFetching fundamentals from Yahoo Finance...")
# fundamentals_yahoo = yahoo_fetcher.fetch_fundamentals(ticker)
# print(fundamentals_yahoo)

print("\nFetching fundamentals from Alpha Vantage...")
fundamentals_alpha = alpha_vantage_fetcher.fetch_fundamentals(ticker)
print(fundamentals_alpha)

# Assuming `df` is a DataFrame obtained from one of the data fetchers.
plotter = FinancialPlotter(df_alpha_vantage)

# To plot the closing price time series:
# plotter.plot_time_series('Close', "AAPL Closing Prices")

# To plot trading volume:
#plotter.plot_volume(title="AAPL Trading Volume")

# To plot an OHLC candlestick chart:
plotter.plot_ohlc()

# To display a correlation matrix of financial metrics:
#plotter.plot_correlation_matrix()

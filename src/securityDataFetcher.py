from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
import requests
import yfinance as yf


class FinancialDataFetcher(ABC):

    @abstractmethod
    def fetch_data(self, ticker: str, start_date: str,
                   end_date: str) -> pd.DataFrame:
        """Fetch historical financial data."""
        pass

    @abstractmethod
    def fetch_fundamentals(self, ticker: str, period: str = "") -> dict:
        """Fetch fundamental financial data for a specific period if applicable."""
        pass


class AlphaVantageDataFetcher(FinancialDataFetcher):

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.BASE_URL = "https://www.alphavantage.co/query"

    def fetch_data(self, ticker: str, start_date: str,
                   end_date: str) -> pd.DataFrame:
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': ticker,
            'apikey': self.api_key,
            'outputsize': 'full'  # Use 'full' for complete data set
        }

        response = requests.get(self.BASE_URL, params=params)
        data = response.json()
        df = pd.DataFrame(data["Time Series (Daily)"])

        df = df.T.rename(
            {
                '1. open': "Open",
                "2. high": "High",
                "3. low": "Low",
                "4. close": "Close",
                "5. volume": "Volume"
            },
            axis='columns')
        df.index = pd.to_datetime(df.index)
        df = df.astype(np.float64)
        df['Volume'] = df['Volume'].astype(np.int32)
        df = df[(df.index >= pd.to_datetime(start_date))
                & (df.index <= pd.to_datetime(end_date))]
        return df

    def fetch_fundamentals(self, ticker: str, period: str = "") -> dict:

        params = {
            "function": "OVERVIEW",
            "symbol": ticker,
            "apikey": self.api_key
        }

        response = requests.get(self.BASE_URL, params=params)
        data = response.json()
        fundamentals = {
            "pe_ratio": float(data.get("PERatio", 0)),
            "market_cap": float(data.get("MarketCapitalization", 0)),
            "dividend_yield": float(data.get("DividendYield", 0)),
            "eps": float(data.get("EPS", 0)),
            "revenue": float(data.get("RevenueTTM", 0))
        }
        return fundamentals


class YahooFinanceDataFetcher(FinancialDataFetcher):

    def fetch_data(self, ticker: str, start_date: str,
                   end_date: str) -> pd.DataFrame:
        data = yf.download(ticker, start=start_date, end=end_date)
        data = data[['Open', 'High', 'Low', 'Adj Close', 'Volume']].rename(columns={'Adj Close': 'Close'})
        return data

    def fetch_fundamentals(self, ticker: str, period: str = "") -> dict:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "pe_ratio": info.get("trailingPE"),
            "market_cap": info.get("marketCap"),
            "dividend_yield": info.get("dividendYield"),
            "eps": info.get("trailingEps"),
            "revenue": info.get("totalRevenue")
        }

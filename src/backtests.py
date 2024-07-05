import numpy as np
import pandas as pd
from strategies import Strategy


def backtest(strategy1: Strategy, strategy2: Strategy, df: pd.DataFrame) -> None:
  buy_signals1, sell_signals1 = strategy1.get_signals(df)
  buy_signals2, sell_signals2 = strategy2.get_signals(df)

  df['Buy1'] = buy_signals1
  df['Sell1'] = sell_signals1
  df['Buy2'] = buy_signals2
  df['Sell2'] = sell_signals2

  df['Strategy1_Position'] = np.where(df['Buy1'], 1, np.where(df['Sell1'], -1, np.nan))
  df['Strategy2_Position'] = np.where(df['Buy2'], 1, np.where(df['Sell2'], -1, np.nan))

  df['Strategy1_Position'] = df['Strategy1_Position'].fillna(method='ffill')
  df['Strategy2_Position'] = df['Strategy2_Position'].fillna(method='ffill')

  df['Strategy1_Returns'] = df['Close'].pct_change() * df['Strategy1_Position']
  df['Strategy2_Returns'] = df['Close'].pct_change() * df['Strategy2_Position']

  strategy1_returns = df['Strategy1_Returns'].cumsum()
  strategy2_returns = df['Strategy2_Returns'].cumsum()

  print(f"Strategy 1 ({strategy1.name}) Returns: {strategy1_returns[-1]}")
  print(f"Strategy 2 ({strategy2.name}) Returns: {strategy2_returns[-1]}")
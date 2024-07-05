from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class Strategy(ABC):

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    def get_signals(self, df: pd.DataFrame) -> tuple:
        raise NotImplementedError(
            "get_signals method must be implemented by child classes")


class MovingAverageStrategy(Strategy):

    def __init__(self, short_window: int, long_window: int) -> None:
        super().__init__("Moving Average", \
                         "Generates buy and sell signals based on moving averages")
        self.short_window = short_window
        self.long_window = long_window

    def get_signals(self, df: pd.DataFrame) -> tuple:
        short_ma = df['Close'].rolling(window=self.short_window).mean()
        long_ma = df['Close'].rolling(window=self.long_window).mean()
        buy_signals = short_ma > long_ma
        sell_signals = short_ma < long_ma
        return buy_signals, sell_signals


class WeightedMovingAverageStrategy(Strategy):

    def __init__(self, short_window: int, long_window: int) -> None:
        super().__init__("Weighted Moving Average", \
                         "Generates buy and sell signals based on weighted moving averages")
        self.short_window = short_window
        self.long_window = long_window

    def get_signals(self, df: pd.DataFrame) -> tuple:
        short_wma = df['Close'].rolling(window=self.short_window).apply(
            lambda x: np.average(x, weights=range(1,
                                                  len(x) + 1)))
        long_wma = df['Close'].rolling(window=self.long_window).apply(
            lambda x: np.average(x, weights=range(1,
                                                  len(x) + 1)))
        buy_signals = short_wma > long_wma
        sell_signals = short_wma < long_wma
        return buy_signals, sell_signals


class ExponentialMovingAverageStrategy(Strategy):

    def __init__(self, short_window: int, long_window: int) -> None:
        super().__init__("Exponential Moving Average", \
                         "Generates buy and sell signals based on exponential moving averages")
        self.short_window = short_window
        self.long_window = long_window

    def get_signals(self, df: pd.DataFrame) -> tuple:
        short_ema = df['Close'].ewm(span=self.short_window,
                                    adjust=False).mean()
        long_ema = df['Close'].ewm(span=self.long_window, adjust=False).mean()
        buy_signals = short_ema > long_ema
        sell_signals = short_ema < long_ema
        return buy_signals, sell_signals

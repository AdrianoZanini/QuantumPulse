import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd


class FinancialPlotter:

    def __init__(self, data: pd.DataFrame, ticker: str):
        """
        Initializes the FinancialPlotter with data.

        :param data: A DataFrame with financial data. The DataFrame should have a DateTimeIndex.
        """
        self.data = data
        self.ticker = ticker

    def apply_dark_theme(self, fig):
        """
        Apply a dark theme to a given Plotly figure.

        :param fig: The Plotly figure to which the dark theme will be applied.
        """
        fig.update_layout(template='plotly_dark',
                          plot_bgcolor='rgba(0, 0, 0, 0)',
                          paper_bgcolor='rgba(0, 0, 0, 0)',
                          font_color='white')
        fig.update_xaxes(showgrid=False, gridwidth=1, gridcolor='DarkGrey')
        fig.update_yaxes(showgrid=False, gridwidth=1, gridcolor='DarkGrey')

    def plot_time_series(self, column='Close', title="Time Series Plot"):
        """
        Plots a time series of the specified column using Plotly with a dark theme.

        :param column: Column name to plot (default is 'Close').
        :param title: Title of the plot.
        """
        fig = px.line(self.data,
                      y=column,
                      title=title,
                      line_shape='linear',
                      render_mode='svg')
        self.apply_dark_theme(fig)
        fig.show()

    def plot_volume(self, title="Volume Over Time"):
        """
        Plots the trading volume over time using Plotly with a dark theme.
        """
        fig = px.bar(self.data, y='Volume', title=title)
        self.apply_dark_theme(fig)
        fig.show()

    def plot_ohlc(self, title="OHLC Candlestick Chart with Volume"):
        ohlc = self.data
        ohlc["previousClose"] = ohlc["Close"].shift(1)
        ohlc["color"] = np.where(ohlc["Close"] > ohlc["previousClose"],
                                 "green", "red")
        ohlc["fill"] = np.where(ohlc["Close"] > ohlc["Open"],
                                "rgba(255, 0, 0, 0)", ohlc["color"])
        ohlc["Percentage"] = ohlc["Volume"] * 100 / ohlc["Volume"].sum()
        price_bins = ohlc.copy()
        price_bins["Close"] = price_bins["Close"].round()
        price_bins = price_bins.groupby("Close",
                                        as_index=False)["Volume"].sum()
        price_bins["Percentage"] = price_bins["Volume"] * 100 / price_bins[
            "Volume"].sum()

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes="columns",
            shared_yaxes="rows",
            column_width=[1],
            row_heights=[0.8, 0.2],
            horizontal_spacing=0,
            vertical_spacing=0,
            subplot_titles=["", "Volume"])
        showlegend = True
        for index, row in ohlc.iterrows():
            color = dict(fillcolor=row["fill"], line=dict(color=row["color"]))
            fig.add_trace(go.Candlestick(x=[index],
                                         open=[row["Open"]],
                                         high=[row["High"]],
                                         low=[row["Low"]],
                                         close=[row["Close"]],
                                         increasing=color,
                                         decreasing=color,
                                         showlegend=showlegend,
                                         name="GE",
                                         legendgroup="Hollow Candlesticks"),
                          row=1,
                          col=1)
            showlegend = False
        fig.add_trace(
            go.Bar(x=ohlc.index,
                   y=ohlc["Volume"],
                   text=ohlc["Percentage"],
                   marker_line_color=ohlc["color"],
                   marker_color=ohlc["fill"],
                   name="Volume",
                   texttemplate="%{text:.2f}%",
                   hoverinfo="x+y",
                   textfont=dict(color="white")),
            col=1,
            row=2,
        )
        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])],
                         rangeslider_visible=False,
                         col=1)
        fig.update_xaxes(showticklabels=True,
                         showspikes=True,
                         showgrid=True,
                         col=2,
                         row=1)
        fig.update_layout(template="plotly_dark",
                          hovermode="x unified",
                          title_text=self.ticker)
        fig.show()

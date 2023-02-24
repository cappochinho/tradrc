#!/usr/bin/env python3
import pandas as pd
import ta

def getdata(client, symbol):
    """
        Retrieves cryptocurrency data using a ticker symbol

        symbol(str): the symbol representing a trading pair
    """
    df = pd.DataFrame(client.get_historical_klines(symbol,
                                                    '15m',
                                                    '3000 minutes UTC'))

    df = df.iloc[:, 0:5]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close']
    df.set_index('Time', inplace=True)
    df.index = pd.to_datetime(df.index, unit='ms')
    df = df.astype(float)
    return df

def indicators(df):
    """
        Determines whether a cryptocurrency is good to buy or not
        Using the SMA of 200 days and a Stochastic RSI strategy
    """
    df['SMA_200'] = ta.trend.sma_indicator(df.Close, window=200)
    df['stochrsi_k'] = ta.momentum.stochrsi_k(df.Close, window=10)
    df.dropna(inplace=True)
    df['Buy'] = (df.Close > df.SMA_200) & (df.stochrsi_k < 0.05)
    return df
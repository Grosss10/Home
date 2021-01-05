"""
Set of functions for the ML approach
"""

import pandas as pd
import numpy as np

import yfinance as yf

yf.pdr_override()
from pandas_datareader import data as pdr

import logging

global curlogger
curlogger = logging.getLogger()


def get_stock_market_data(stock_symbol, start, end):
    """
    @param stock_symbol:
    @param start:
    @param end:

    """
    df_raw = pdr.get_data_yahoo(stock_symbol, start=start, end=end)
    df_raw.reset_index(level=0, inplace=True)
    df_raw = df_raw.rename(columns={'Open':'Value'})
    df = df_raw[['Date', 'Value']]
    df.insert(2,'Symbol',stock_symbol)

    ticker = yf.Ticker(stock_symbol)
    info = (ticker.info)
    print(info['longName'])

    return df

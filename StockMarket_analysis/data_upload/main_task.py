# -*- coding: utf-8 -*-
"""
This is a collection of functions to run the main task
"""

import os
import pandas as pd
import logging

import yfinance as yf
yf.pdr_override()
from pandas_datareader import data as pdr
from StockMarket_analysis.data_upload import functions as fun
from StockMarket_analysis.general_operations import general_configs as gc
import matplotlib.pyplot as plt

global curlogger
curlogger = logging.getLogger()


def main_task(folder, config_container):
    """
    This function executes the upload of stock data
    """

    #variables
    stock_symbol = config_container.stock_symbol
    platform = config_container.platform
    start = gc.period["start"]
    end = gc.period["end"]

    ###
    #start with main task
    ###
    msg = 'working with stock: %s' %stock_symbol
    curlogger.info(msg)
    print(msg)


    #retrieve dataframe of stock
    if platform == "yahoo":
        df = fun.get_stock_market_data(stock_symbol, start, end)
        msg = 'successfully retrieved data from %s' %platform
        curlogger.info(msg)
        print(msg)
    else:
        msg = '%s is an unknown platform, no data retrieved for %s' %(platform,stock_symbol)
        curlogger.warning(msg)
        print(msg)

    #Todo: upload dataframe to database

    #plot figure
    if not df.empty:
        df.plot(x="Date", y="Value", title=stock_symbol,kind='line', legend =False,rot='vertical')
        plt.show()


    ###
    #Done!
    ###
    msg = "Done!"
    curlogger.info(msg)
    print(msg)

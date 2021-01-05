"""
This are routines for the  main task running before the actual main task
"""
import logging
import os

from StockMarket_analysis.general_operations import general_configs as gc
global curlogger
curlogger = logging.getLogger()


def preparatory_tasks(folder):
    """
    some standard task before we run the main task
    """
    # create destination folder if necessary
    if not os.path.isdir(folder):
        os.makedirs(folder)

    # get the symbol of the stock
    stock_symbol = os.path.split(folder)[1]

    # get plattform to download stockdata
    platform = gc.platform

    return stock_symbol,platform
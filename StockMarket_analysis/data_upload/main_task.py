# -*- coding: utf-8 -*-
"""
This is a collection of functions to run the main task
"""

import os
import pandas as pd

import logging
from StockMarket_analysis.data_upload import functions as fun
from StockMarket_analysis.general_operations import general_configs as gc

global curlogger
curlogger = logging.getLogger()


def main_task(folder, config_container):
    """
    This function executes the upload of stock data
    """


    ###
    #start with main task
    ###

    #Done!
    msg = "Done!"
    curlogger.info(msg)
    print(msg)

# -*- coding: utf-8 -*-
from __future__ import print_function



"""
Created on Jan 2021

@Autor Simon Gross
"""

from time import sleep
import pandas
from guidata.dataset.datatypes import DataSet, DataSetGroup
from first_tab import first_tab


class RunWorkflows(DataSet):
    """
    My Home analysis
    *tab1 includes stock market analysis, identifier is name of stock, check out metadata.

    """


if __name__ == "__main__":
    # prepare the gui app
    import guidata

    _app = guidata.qapplication()
    # e = RunWorkflows()
    e1 = first_tab("Stock Market")
    e = DataSetGroup([e1], title='Home Analysis')
    # show the gui and proceed further if the user presses OK.
    if e.edit():
        # file with session to analyze
        experiments_to_analyze = e1.experiments_to_analyze
        if e1.sleep_hours:
            print("Sleeping for %s hours" % str(e1.sleep_hours))
            stime = e1.sleep_hours * 60 * 60
            sleep(stime)

        # import all the stuff we need from freely moving
        import logging
        from StockMarket_analysis.data_upload.workflow import workflow

        # let's log options introduced by the user
        curlogger = logging.getLogger()
        msg = "Experiments to analyze file: %s" % experiments_to_analyze
        curlogger.info(msg)
        print(msg)
        msg = "Workflows selected to be run:"
        curlogger.info(msg)
        print(msg)


        msg = "Run the ML tasks: %s" % e1.item1_upload_data
        curlogger.info(msg)
        print(msg)

        # upload of stock market data
        if e1.item1_upload_data:
            msg = "run workflow=%s" % e1.item1_upload_data
            curlogger.info(msg)
            print(msg)
            workflow = workflow(folders_to_analyze_file=experiments_to_analyze)
            workflow.run_workflow()

        msg = "Done! Quitting the application!"
        curlogger.info(msg)
        print(msg)

"""
This are routines for the  main task running before the actual main task
"""
import logging
import os

global curlogger
curlogger = logging.getLogger()


def preparatory_tasks(folder):
    """
    some standard task before we run the main task
    """

    session_path = folder

    return session_path
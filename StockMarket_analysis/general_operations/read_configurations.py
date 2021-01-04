from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function

"""
This module is focus on reading and checking the validity of configurations for the worklow,
coming from files (or databases in the future).
"""

import logging
import os
import pandas as pd

from StockMarket_analysis.general_operations import general_configs as gc

global curlogger
curlogger = logging.getLogger()


##
#Functions to read configuration files

def folder_file_to_folders_list(folder_file):
    """
    This function reads a folder file ( a text file containing the folders to be analyzed )
    to a list of existing full path to those folders.
    If a folder does not exist a warning is printed.
    :param folder_file: string : path to the folder txt file
    :return:
    """

    root = gc.data_root_folder
    f = open(folder_file)
    folders_list = list()
    for line in f:
        curfolder = os.path.join(root,line.strip())
        if os.path.isdir(curfolder):
            folders_list.append(curfolder)
        else:
            msg = "%s folder not found!" % curfolder
            curlogger.error(msg)
            print(msg)
    f.close()
    return folders_list


##
#Functions to check the existence and validity of configuration files

def check_and_get_metadata_file(path_to_file,sep=None):
    """
    Function to read the metadata file, and check that it is correct. It also adds the animal column.
    :rtype:
    :param path_to_file: string: path to the metadata file (csv)
    :param sep: separator of the csv, by default None, which mean guess, otherwise can be something like ",", "\t" etc
    :return:
    df: pandas dataframe with the metadata

    Raises exception if the columns in the csv do not match what is expected.
    
    """

    #read the file in one go with pandas
    df = pd.read_csv(path_to_file,sep=sep,engine='python')
    #check that all the expected columns are there
    expected_columns = ['Species', 'Genotype', 'Intracranial recording site', 'Compound', 'RO Number', 'Concentration',
                        'Route of administration', 'Vehicle', 'Date compound tested','Quality','Electrode type',
                        'Recording instrument', 'Study id', 'Unit quality', 'Compound code','Varia_1','Varia_2','Varia_3','Varia_4']
    actual_columns = df.columns.values.tolist()
    expected_columns = [x.lower() for x in expected_columns]
    actual_columns = [x.lower() for x in actual_columns]
    if not set(expected_columns) == set(actual_columns):
        msg = "Expected and actual column names do not match for metafile data %s" %path_to_file
        raise Exception(msg)
    df.columns = actual_columns
    #add the animal column
    animals = df["date compound tested"].str.split("_").str[0]
    df["animal"] = animals

    return df

def get_folders_and_metadata(path_to_folders_file, recording_area_filter=None):
    """
    Checks that all the folders (date_compound_tested) are registered in the metadata table. It raises an exception
    if not. Then it filters out folders not belonging to the current brain area filter.
    :param path_to_folders_file: string: path to csv containing folders, one per line
    :returns: folders_to_analyze: list<string>: path to the folders to be analyzed
              metadata: pandas dataframe with the metadata for the current folders
    raises exception if finds that a folder is not registered in the metadata table.
    Raises exception if after filtering no rows are left (not filtered), meaning there is nothing to be analyzed
    """

    #read the folders file
    folders = list()
    f = open(path_to_folders_file)
    for line in f:
        line = line.strip()
        if line:
            if len(line.split())>1:
                msg = "malformed file, only 1 folder per line allowed %s" % path_to_folders_file
                raise Exception(msg)
            folders.append(line)
    f.close()

    #prepare the folders to analyze
    folders_to_analyze = list()

    #iterate trough folders in order to keep the original sorting
    for exp_folder in folders:
        folders_to_analyze.append(os.path.join(gc.data_root_folder,exp_folder))

    metadata = None

    return folders_to_analyze, metadata

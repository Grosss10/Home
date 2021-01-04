from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function

"""
This module contains the abstract class to use as template for all workflows
written by Otto Fajardo (otto.fajardo@roche.com) on 29.08.2016
"""

import abc
import logging
import os
import traceback
import getpass

from StockMarket_analysis.general_operations import general_configs as gc
from StockMarket_analysis.general_operations.ConfigurationsContainer import ConfigurationsContainer
from StockMarket_analysis.general_operations import read_configurations

global curlogger
curlogger = logging.getLogger()


class AbstractWorkflow(object):
    """
    This class should be used as template for all workflows. It defines some methods that will be common for all
    workflows, some that must be defined by the children classes and some optional.
    The ones that must be defined are indicated by the NotImplementedError. Please read the documentation of the
    methods to understand what they do.
    The run_workflow method is the one that is going to be called to execute a workflow and therefore contains
    the sequence of events that are going to be executed.
    """

    __metaclass__ = abc.ABCMeta
    def __init__(self, folders_to_analyze_file = None):
        if folders_to_analyze_file:
            self.folders_to_analyze_file = folders_to_analyze_file
        else:
            raise Exception("Please indicate a folders_to_analyze_file")
        #initialize config_container
        self.config_container = None
        # Prohibit creating class instance from this abstract workflow
        if self.__class__ is AbstractWorkflow:
            raise TypeError('abstract class cannot be instantiated')

    #default methods: the same for all workflows

    def read_folders_and_metadata(self, config_container):
        """
        This method reads the metadata file and extracts both the metadata and folders to be analyzed.
        :param config_container: instance of ConfigurationsContainer
        """

        folders_to_analyze_file = os.path.join(gc.data_root_folder, self.folders_to_analyze_file)
        folders_to_analyze, metadata = read_configurations.get_folders_and_metadata(folders_to_analyze_file)
        config_container.folders_to_analyze = folders_to_analyze
        config_container.metadata = metadata

    ##
    #optional methods: children workflows can choose if override or not, by default do nothing

    def initial_operations(self, config_container):
        """
        This method will be executed after reading the metadata and before looping through the folders. Can be overriden
        for doing things with the metadata, preparation of things before looping, etc.
        It should not return anything, everything that needs re-use in other methods should be put in config_container.
        :param config_container: instance of ConfigurationsContainer

        """
        pass

    def read_extra_configurations(self,folder,config_container):
        """
        This method will contain reading other configuration or data files needed for the specific workflow.
        It should not return anything, everything that needs re-use in other methods should be put in config_container.
        :param folder: path to the current folder being analyzed
        :param config_container: instance of ConfigurationsContainer
        :return:
        """
        pass

    def check_configurations(self, folder, config_container):
        """
        This method will check that all the configurations are OK before executing the workflow main method for the
        folder.
        It should not return anything, everything that needs re-use in other methods should be put in config_container.
        :param folder: path to the current folder being analyzed
        :param config_container: instance of ConfigurationsContainer

        """
        pass

    def get_class_name(self):
        """
        This method prints the name of the current class. Children classes must implement it if the name of the child
        class should be correctly printed in the logs.
        :return:
        """
        # if you call self.__class__.__name__ diretly from run_workflow, then you get printed AbstractWorkflow in the logs,
        # altough printing to the console is correct. Who knows why!
        return self.__class__.__name__


    ##
    #must re-implement methods: children workflows must override those!

    @abc.abstractmethod
    def main_workflow_method(self,folder, config_container):
        """
        This method is the main method of the workflow, the actual analysis executed on a folder.
        It should not return anything, everything that needs re-use in other methods should be put in config_container.
        :param folder: path to the current folder being analyzed
        :param config_container: instance of ConfigurationsContainer

        """
        return


    ##
    # execution entry point, this is also default and is what is going to be executed

    def run_workflow(self):
        """
        This is the main entry point of the class, this will execute the whole workflow over all folders
        :return:
        """
        try:
            msg = " " * 80
            print(msg)
            curlogger.info(msg)
            msg = "Running Workflow Class: %s" % self.get_class_name()
            curlogger.info(msg)
            print(msg)
            msg = "user: %s" % getpass.getuser()
            curlogger.info(msg)
            print(msg)
            msg = " " * 80
            print(msg)
            curlogger.info(msg)
            #congif_container is a container for all configurations that should be passed from one method to the other
            self.config_container = ConfigurationsContainer()
            ##start!
            #read the folders and check that all of them are in the metadata table
            self.read_folders_and_metadata(self.config_container)
            #execute initial operations
            self.initial_operations(self.config_container)
            #result_status will contain the OK or Fail for every folder
            result_status = list()
            #Now loop through all folders
            folders = self.config_container.folders_to_analyze
            for indx,folder in enumerate(folders):
                msg = " " * 80
                print(msg)
                curlogger.info(msg)
                msg = "=" * 80
                print(msg)
                curlogger.info(msg)
                msg = " " * 80
                print(msg)
                curlogger.info(msg)
                msg = "Processing folder %d of %d" % (indx+1, len(folders))
                curlogger.info(msg)
                print(msg)
                msg = "Folder: %s" % folder
                curlogger.info(msg)
                print(msg)
                try:
                    #This is what is executed for every folder: read default configurations, extra configurations defined
                    #by the child workflow, checkings on those configurations and then we execute the main method
                    self.read_extra_configurations(folder, self.config_container)
                    self.check_configurations(folder, self.config_container)
                    self.main_workflow_method(folder, self.config_container)
                    result_status.append((folder, "OK"))

                except:
                    tb = traceback.format_exc()
                    msg = "An Error ocurred, skipping folder, stacktrace:\r\n%s" % tb
                    curlogger.error(msg)
                    print(msg)
                    result_status.append((folder, 'FAILED'))

            # log the results
            msg = " " * 80
            print(msg)
            curlogger.info(msg)
            msg = "*" *80
            curlogger.info(msg)
            print(msg)
            msg = " " * 80
            print(msg)
            curlogger.info(msg)
            msg = "Summary of %s results" % self.get_class_name()
            curlogger.info(msg)
            print(msg)
            for row in result_status:
                msg = "folder: " + row[0] + " status: " + row[1]
                curlogger.info(msg)
                print(msg)
            msg = " " * 80
            print(msg)
            curlogger.info(msg)
            msg = "*" *80
            curlogger.info(msg)
            print(msg)

        except:
            tb = traceback.format_exc()
            msg = "An Error ocurred, aborting procedure, stacktrace:\r\n%s" % tb
            curlogger.error(msg)
            print(msg)
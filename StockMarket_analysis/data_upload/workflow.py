"""
workflow for stock analysis
"""

import logging

from StockMarket_analysis.general_operations.AbstractWorkflow import AbstractWorkflow
from StockMarket_analysis.data_upload.main_task import main_task
from StockMarket_analysis.data_upload.preparatory_tasks import preparatory_tasks


global curlogger
curlogger = logging.getLogger()



class workflow(AbstractWorkflow):
    """
    This class implements the workflow for retrieving stock data.
    """

    def __init__(self,folders_to_analyze_file=None):

        super(workflow, self).__init__(folders_to_analyze_file = folders_to_analyze_file)

    def get_class_name(self):
        """
        Override this method in the parent class to have a correctly printed name of the child class in the logs.
        :return:
        """
        return self.__class__.__name__

    def check_configurations(self, folder, config_container):
        """
        Set of Rules to check for the configurations of the workflow, and also sets important fields to config_container
        that later are going to be used by the workflow: trial_sessions, plexon_files, good_channels
        :param folder: path to the current workflow being analyzed
        :param config_container: Instance of ConfigurationsContainer
        """

        session_path = preparatory_tasks(folder)
        config_container.session_path = session_path

    def main_workflow_method(self, folder, config_container):
        """
        This will execute the workflow
        :param folder: path to the current workflow being analyzed
        :param config_container: Instance of ConfigurationsContainer
        """
        main_task(folder, config_container)

if __name__ == "__main__":
    workflow = workflow()
    workflow.run_workflow()





"""
This module contains the Configuration container to be used with every workflow.
written by Otto Fajardo (otto.fajardo@roche.com) on 29.08.2016
"""


class ConfigurationsContainer:
    """
    This class will act as a container to store configuration elements that need to be passed from one workflow
    method to the other.
    """

    def __init__(self):
        """
        We pre-defined some fields that will always be there, but the user can introduce more as needed.
        """
        # list of all folders to be analyzed
        self.folders_to_analyze = None
        # metadata
        self.metadata = None


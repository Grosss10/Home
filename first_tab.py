SHOW = True  # Show test in GUI-based test launcher

import os
from guidata.dataset.datatypes import ActivableDataSet, ValueProp, EndGroup, BeginGroup
from guidata.dataset.dataitems import BoolItem, FloatItem, FileOpenItem
from StockMarket_analysis.general_operations import general_configs as gc


class first_tab(ActivableDataSet):

    # stock market analysis
    runuploaddata = ValueProp(False)

    enable = BoolItem("Enable parameter set", help="If disabled, the following parameters will be ignored",
                      default=False)

    default_exps_file = os.path.join(gc.data_root_folder, gc.default_exps_file)
    experiments_to_analyze = FileOpenItem("Stocks to analyze", formats=["csv"], basedir=gc.data_root_folder,
                                          default=default_exps_file)

    # Sleep
    sleep_help = "the application will sleep for the indicated amount of hours before starting with the processing"
    sleep_hours = FloatItem("Delay start (hours)", help=sleep_help, slider=True, min=0, max=48, default=0)

    ###
    #Begin of groups
    ###


    sg1 = BeginGroup("Uploading Chart Data")
    # xxx
    item1_upload_data = BoolItem("Upload Data").set_prop("display", store=runuploaddata)

    _sg1 = EndGroup("Uploading Chart Data")

    ###
    #End of groups
    ###

first_tab.active_setup()

if __name__ == '__main__':
    # Create QApplication
    import guidata

    _app = guidata.qapplication()

    # Editing mode:
    prm = first_tab()
    prm.set_writeable()
    prm.edit()

    # Showing mode:
    prm.set_readonly()
    prm.view()

import os
import json
import pandas as pd

from collections import defaultdict
from app.library.ingest import ingest as ingest
from app.library.data.prepare import create_data_signalbase
from icecream import ic

class Signals():
    def __init__(self):
        temp_path = os.path.join(os.getcwd(), r'app\library\config')
        self.config_path = self.check_path_exists(temp_path)
        self.defaults = self.load_defaults('signals.json')
    
    def load_defaults(self, file_name):
        path = os.path.join(self.config_path, file_name)
        
        ret_val: defaultdict(dict)
        ret_val = self.read_json_file(path)
        
        return ret_val

    def read_json_file(self, path):
        ret_val = None
        with open(path) as file:
            content = file.read()
            json_val = json.loads(content)
            ret_val = dict(json_val)
        return ret_val

    def check_path_exists(self, path):
        if os.path.exists(path):
            return path
        else:
            raise FileNotFoundError(f'{path} directory not found')






def signal_data_selection(
 #       signal_int:int, 
        preset,
        array_data,
        side,
        pre_processing = 'euclidean',
        legs = 'both'):
    """   
    Args: signal preset selected by user
    This function should be called after the user has selected a preset
    Has to have input datafiles before
    array_data, side: from previous route ingest

    Returns: signal_data_selection, signal_names

    """


    

    
    n_list = list()        
    n_list.append(5)

    signal_data_selection, _= create_data_signalbase(
        array_data,   # main data input (array_data bei ingest.load_matlab_csv()
        preset,          # load_preset_signals()-------------------------------------
        side,
        n_list,
        pre_processing=pre_processing,
        do_norm=None,
        legs=legs
        )
    
    return signal_data_selection




def create_checkboxes_signals(data):
    temp_checkbox = {}
    col_names = [x[0] for x in data.columns]
    col_names = list(dict.fromkeys(col_names))

    other = [str(x) for x in col_names if 'angles' not in str(x).lower() and 'moment' not in str(x).lower() and 'power' not in str(x).lower()]
    ic(other)
    angle_moment_values = [str(x) for x in col_names if 'angles' in str(x).lower() or 'moment' in str(x).lower()]
    power_values = [str(x) for x in col_names if 'power' in str(x).lower()]

    temp_checkbox['angle_moment_values'] = {}
    for ang_mom in angle_moment_values:
        temp_checkbox['angle_moment_values'][ang_mom] = {
            'enabled': False,
            'sag': False,
            'front': False,
            'trans': False,
        }

    temp_checkbox['power_values'] = {}
    for power_val in power_values:
        temp_checkbox['power_values'][power_val] = {
            'enabled': False,
            'sag': False,
            'front': False,
            'trans': False,
        }


    return temp_checkbox
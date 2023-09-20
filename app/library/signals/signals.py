import os
import json
import pandas as pd

from collections import defaultdict
from app.library.ingest import ingest as ingest
from app.library.data.prepare import create_data_signalbase

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









def get_signals():   # return list signal_names of json signals, the keys of the array

    signals = Signals()
    signal_dict = signals.defaults
    signal_names = list(signal_dict.keys())


    return signal_dict, signal_names

def get_preset(signal_dict, signal_names, test_key:int):
    preset_val = signal_names[test_key]
    preset = signal_dict[preset_val]
    print(preset)
    return preset

def signal_data_selection(
        signal_int:int, 
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

    signal_dict, signal_names = get_signals()
    preset = get_preset(signal_dict, signal_names, signal_int)
    n_list = list()         # list of signal keys, should be customizable, but is always one int //Subsampling rate, same as in execute_models
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
    return signal_data_selection, signal_names




def create_checkboxes_signals(data):
    temp_checkbox = {}
    col_names = [x[0] for x in data.columns]
    col_names = list(dict.fromkeys(col_names))

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
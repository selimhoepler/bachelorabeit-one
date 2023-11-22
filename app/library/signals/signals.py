"""
This module provides functionalities for processing and handling signal data. 
It includes functions for selecting signal data based on user presets and creating a structured format for checkbox inputs 
in the user interface.

Functions:
- signal_data_selection(preset, array_data, side, pre_processing, legs): Selects signal data based on user-defined presets.
- create_checkboxes_signals(data): Generates a structured format for checkbox inputs based on data column names.
"""

import os
import json
import pandas as pd

from collections import defaultdict
from app.library.ingest import ingest as ingest
from app.library.data.prepare import create_data_signalbase
from icecream import ic

# class Signals():
#     def __init__(self):
#         temp_path = os.path.join(os.getcwd(), r'app\library\config')
#         self.config_path = self.check_path_exists(temp_path)
#         self.defaults = self.load_defaults('signals.json')
    
#     def load_defaults(self, file_name):
#         path = os.path.join(self.config_path, file_name)
        
#         ret_val: defaultdict(dict)
#         ret_val = self.read_json_file(path)
        
#         return ret_val

#     def read_json_file(self, path):
#         ret_val = None
#         with open(path) as file:
#             content = file.read()
#             json_val = json.loads(content)
#             ret_val = dict(json_val)
#         return ret_val

#     def check_path_exists(self, path):
#         if os.path.exists(path):
#             return path
#         else:
#             raise FileNotFoundError(f'{path} directory not found')






def signal_data_selection(
        preset,
        array_data,
        side,
        pre_processing = 'euclidean',
        legs = 'both'):
    
    """   
    Args:   
    - preset (dict) : signal preset selected by user 
    - array_data (pd.Dataframe): preprocessed dataframe with GAIT data
    - side (numpy array): array with specification on which side is affected (0=R, 1=L, 2=Both)  


    Returns: 
    - signal_data_selection (dict): Dictionary containing the selected signal data

    """


    

    
    n_list = list()        
    n_list.append(5)

    signal_data_selection, _= create_data_signalbase(
        array_data,  
        preset,          
        side,
        n_list,
        pre_processing=pre_processing,
        do_norm=None,
        legs=legs
        )
    
    return signal_data_selection




def create_checkboxes_signals(data):
    """
    Creates a structured format for checkbox inputs based on the column names in the provided DataFrame. 

    The checkboxes are categorized into 'angle_moment_values' and 'power_values' based on the column name contents.

    Args:
    - data (pd.DataFrame): DataFrame containing GAIT data.

    Returns:
    - temp_checkbox (dict): A dictionary structured for checkbox inputs with categories and options.
    """


    # Extracting column names and removing duplicates
    col_names = [x[0] for x in data.columns]
    col_names = list(dict.fromkeys(col_names))

    # Categorizing columns based on keywords
    angle_moment_values = [str(x) for x in col_names if 'angles' in str(x).lower() or 'moment' in str(x).lower()]
    power_values = [str(x) for x in col_names if 'power' in str(x).lower()]

    # Creating checkbox structures for each category
    temp_checkbox = {'angle_moment_values': {}, 'power_values': {}}

    for ang_mom in angle_moment_values:
        temp_checkbox['angle_moment_values'][ang_mom] = {
            'enabled': False,
            'sag': False, 
            'front': False, 
            'trans': False
            }

    for power_val in power_values:
        temp_checkbox['power_values'][power_val] = {
            'enabled': False, 
            'sag': False, 
            'front': False, 
            'trans': False
            }

    return temp_checkbox

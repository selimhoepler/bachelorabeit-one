"""
This module provides utilities for saving and loading data in various formats including pickle and JSON. 
It is designed to handle operations related to saving and loading GAIT data, metadata, and other related information 
used in the application. The module includes functions to save data to and load data from pickle files, 
convert data to JSON format, and replace NaN values in the data.

Functions:
- savePickle: Saves dataframes to pickle files.
- loadPickle: Loads dataframes from pickle files.
- saveDict: Saves a dictionary to a pickle file.
- loadDict: Loads a dictionary from a pickle file.
- saveJSON: Saves a dataframe as a JSON file.
- replace_nan: Replaces NaN values in the given data with zeros.
"""

import pickle
import os
import json, numpy as np
import math

# Path to .pkl and .json files
pickle_path = r"app\temp"
json_path = r"static\json"

def savePickle(array_data, meta_data, side, scalar_data):

    """
    Saves the provided dataframes and side array to pickle files at a specified path.

    Args:
    - array_data (pd.DataFrame): Dataframe containing array data.
    - meta_data (pd.DataFrame): Dataframe containing metadata.
    - side (np.array): Array indicating sides relevant to the data.
    - scalar_data (pd.DataFrame): Dataframe containing scalar data.
    """


    with open(os.path.join(pickle_path, "array_data.pkl"), "wb") as f:
        pickle.dump(array_data, f)

    with open(os.path.join(pickle_path, "meta_data.pkl"), "wb") as f:
        pickle.dump(meta_data, f)

    with open(os.path.join(pickle_path, "side.pkl"), "wb") as f:
        pickle.dump(side, f)

    with open(os.path.join(pickle_path, "scalar_data.pkl"), "wb") as f:
        pickle.dump(scalar_data, f)


    
def loadPickle():
   
    """
    Loads dataframes from pickle files located at a specified path.

    Returns:
    - tuple: Contains loaded dataframes (array_data, meta_data, side, scalar_data).
    """
       

    with open(os.path.join(pickle_path, "array_data.pkl"), "rb") as f:
        array_data = pickle.load(f)

    with open(os.path.join(pickle_path, "meta_data.pkl"), "rb") as f:
        meta_data = pickle.load(f)

    with open(os.path.join(pickle_path, "side.pkl"), "rb") as f:
        side = pickle.load(f)
    
    with open(os.path.join(pickle_path, "scalar_data.pkl"), "rb") as f:
        scalar_data = pickle.load(f)

        print(f'Scalar_data is type: {type(scalar_data)}')

    return array_data, meta_data, side, scalar_data




def saveDict(dict, name:str):
    with open(os.path.join(pickle_path, f"{name}.pkl"), "wb") as f:
        pickle.dump(dict, f)

def loadDict(name:str):
    with open(os.path.join(pickle_path, f"{name}.pkl"), "rb") as f:
        dict = pickle.load(f)
    return dict


class NumpyEncoder(json.JSONEncoder):
    """
    Custom JSON encoder subclass that handles NumPy data types.

    This encoder extends the standard `json.JSONEncoder` class to convert NumPy data types 
    into native Python types that can be serialized into JSON. This is particularly useful 
    for converting NumPy numerical types that are not natively serializable by the standard 
    JSON encoder.

    Methods:
    - default(obj): Overrides the default method to handle NumPy data types.
    """
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, np.int64):
            return int(obj)
        return super().default(obj)
    
def saveJSON(dataframe, filename: str):
    """
    Saves the dataframe as a JSON file at the specified path.
    
    Args:
    -   dataframe (pd.DataFrame): The dataframe to save.
    """
    # Convert the DataFrame to a JSON string
    json_string = dataframe.to_json(orient='split', index=False)
    
    # Define the file path
    file_path = os.path.join(json_path, filename)
    
    # Write the JSON string to a file
    with open(file_path, "w") as f:
        json.dump(json.loads(json_string), f)


def replace_nan(data):
    """
    Replaces NaN values in the given data.

    Args:
    - data (list of dict): The input data containing dictionaries with potential NaN values.

    Returns:
    - list of dict: The modified data with NaN values replaced.
    """
    for item in data:
        if math.isnan(item['x']):
            item['x'] = 0
        if math.isnan(item['y']):
            item['y'] = 0
    return data



    


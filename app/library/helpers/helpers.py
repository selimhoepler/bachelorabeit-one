import pickle
import os
import json, numpy as np
import math

# Pfad zum gewünschten Speicherort der pickle-Dateien
pickle_path = r"app\temp"
json_path = r"static\json"

def savePickle(array_data, meta_data, side, scalar_data):
    # Speichern der DataFrames


# Speichern der DataFrames am angegebenen Speicherort
    with open(os.path.join(pickle_path, "array_data.pkl"), "wb") as f:
        pickle.dump(array_data, f)

    with open(os.path.join(pickle_path, "meta_data.pkl"), "wb") as f:
        pickle.dump(meta_data, f)

    with open(os.path.join(pickle_path, "side.pkl"), "wb") as f:
        pickle.dump(side, f)

    with open(os.path.join(pickle_path, "scalar_data.pkl"), "wb") as f:
        pickle.dump(scalar_data, f)
    
def loadPickle():
    # load the data from the pickle files and return them
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
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, np.int64):
            return int(obj)
        return super().default(obj)
    
def saveJSON(dataframe, filename: str):
    """
    Saves the dataframe as a JSON file at the specified path.
    
    Parameters:
    dataframe (pd.DataFrame): The dataframe to save.
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



    


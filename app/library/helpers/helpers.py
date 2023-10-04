import pickle
import os
import json, numpy as np

# Pfad zum gewünschten Speicherort der pickle-Dateien
pickle_path = r"app\temp"
json_path = r"app\temp\json"

def savePickle(array_data, meta_data, side):
    # Speichern der DataFrames


# Speichern der DataFrames am angegebenen Speicherort
    with open(os.path.join(pickle_path, "array_data.pkl"), "wb") as f:
        pickle.dump(array_data, f)

    with open(os.path.join(pickle_path, "meta_data.pkl"), "wb") as f:
        pickle.dump(meta_data, f)

    with open(os.path.join(pickle_path, "side.pkl"), "wb") as f:
        pickle.dump(side, f)

    
def loadPickle():
    # load the data from the pickle files and return them
    with open(os.path.join(pickle_path, "array_data.pkl"), "rb") as f:
        array_data = pickle.load(f)

    with open(os.path.join(pickle_path, "meta_data.pkl"), "rb") as f:
        meta_data = pickle.load(f)

    with open(os.path.join(pickle_path, "side.pkl"), "rb") as f:
        side = pickle.load(f)

    return array_data, meta_data, side

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
    
def saveJSON(dataframe):
    # Save the DataFrame as a JSON file
    
    dataframe.to_json(json_path, orient='split', index=False)

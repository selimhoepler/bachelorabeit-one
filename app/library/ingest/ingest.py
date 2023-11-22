"""
This module provides functions to process and analyze data exported from MATLAB. 
It includes functionality to read MATLAB-generated CSV files, handle scalar and array data, and prepare data for further analysis.

Functions:
- represents_int(s): Check if a string represents an integer.
- load_matlab_csv(filename, scalar_and_array): Read MATLAB-generated CSV files into DataFrames.
- get_datas(data_filename, metadata_filename): Process data and metadata files for analysis.

The module is used in the function upload_files from route @ingest

"""


import pandas as pd
import numpy as np
from icecream import ic



def represents_int(s):

    # checks if the given parameter is an integer
    # returns bool

    try:
        int(s)
        return True
    except ValueError:
        return False



def load_matlab_csv(filename, scalar_and_array=True):

    """Read CSV written by matlab tablewrite into DataFrames

    Each entry in the table can be a scalar or a variable length array.
    If it is a variable length array, then Matlab generates a set of
    columns, long enough to hold the longest array. These columns have
    the variable name with an index appended.

    This function infers which entries are scalars and which are arrays.
    Arrays are grouped together and sorted by their index.

    Args:
        filename (str): Path to the CSV file.
        scalar_and_array (bool): Flag to determine if both scalar and array data should be processed.
                                 If False, only scalar data is returned.

    Returns: scalar_df, array_df
        scalar_df : DataFrame of scalar values from the table
        array_df : DataFrame with MultiIndex on columns
            The first level is the array name
            The second level is the index within that array
    """



    # Read the CSV file
    tdf = pd.read_table(filename, sep=',', low_memory=False)
    cols = list(tdf.columns)

    # Figure out which columns correspond to scalars and which to arrays
    scalar_cols = []  # scalar column names
    arr_cols = []  # array column names, without index
    arrname2idxs = {}  # dict of array column name to list of integer indices
    arrname2colnames = {}  # dict of array column name to list of full names

    # Iterate over columns
    for col in cols:
        # If the name ends in "_" plus space plus digits, it's probably
        # from an array
        if col[-1] in '0123456789' and '_' in col and scalar_and_array:
            # Array col
            # Infer the array name and index
            colsplit = col.split('_')
            arr_idx = int(colsplit[-1])
            arr_name = '_'.join(colsplit[:-1])

            # Store
            if arr_name in arrname2idxs:
                arrname2idxs[arr_name].append(arr_idx)
                arrname2colnames[arr_name].append(col)
            else:
                arrname2idxs[arr_name] = [arr_idx]
                arrname2colnames[arr_name] = [col]
                arr_cols.append(arr_name)

        else:
            # Scalar col
            scalar_cols.append(col)

    # Extract all scalar columns
    scalar_df = tdf[scalar_cols]

    array_df = []
    if scalar_and_array:
        # Extract each set of array columns into its own dataframe
        array_df_d = {}
        for arrname in arr_cols:
            adf = tdf[arrname2colnames[arrname]].copy()
            adf.columns = arrname2idxs[arrname]
            array_df_d[arrname] = adf

        # Concatenate array dataframes
        array_df = pd.concat(array_df_d, axis=1)

    return scalar_df, array_df


def get_datas(data_filename, metadata_filename):

    """
    Processes data and metadata files, setting 'Session_ID' as the index and filtering metadata for specific use cases.

    Args:
        data_filename (str): The filename for the data CSV file.
        metadata_filename (str): The filename for the metadata CSV file.

    Returns:
        array_data (pd.DataFrame): Processed data with 'Session_ID' as the index.
        meta_data (pd.DataFrame): Filtered metadata set to the index of 'scalar_data'.
        side (np.array): Array indicating if the data is relevant for the left, right, or both sides of the patient.
        scalar_data (pd.DataFrame): Scalar data with 'Session_ID' as the index.
    """



    scalar_data, array_data = load_matlab_csv(data_filename)


    # set 'Session_ID' as column from scalar_data
    array_data['Session_ID'] = scalar_data.loc[:, 'Session_ID']

    # set 'Session_ID' as index for array and scalar df
    array_data = array_data.set_index('Session_ID')
    scalar_data = scalar_data.set_index('Session_ID', drop=False)


    meta_data, _ = load_matlab_csv(metadata_filename, scalar_and_array=False)

    # set 'DBid' as Index (same form as 'Session_ID')
    meta_data = meta_data.set_index('DBid')

    # selecting only those metadata that are considered for UC1 (patients with axial malalignments) from scalar index
    meta_data = meta_data.loc[scalar_data.index, :]




    # This is a NumPy array that stores information about whether the data is relevant for the right or left side (or both) of the patient.
    # This information is derived from the columns UC1_affected_RE and UC1_affected_LI columns in meta_data.

    side = np.ones(meta_data.UC1_betroffen_RE.shape[0])*(-1)
    side[meta_data.UC1_betroffen_LI == 1] = 0
    side[meta_data.UC1_betroffen_RE == 1] = 1
    side[
        (meta_data.UC1_betroffen_LI == 1) &
        (meta_data.UC1_betroffen_RE == 1)
    ] = 2


    # info printing
    ic(f'[INFO] container.side length: {len(side)}')
    ic(f'[INFO] container.data length: {len(array_data)}')
    ic(f'[INFO] container.meta_data length: {len(meta_data)}')



    return array_data, meta_data, side, scalar_data


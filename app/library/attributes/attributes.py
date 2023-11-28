"""
This module contains functions for processing and extracting specific attributes from metadata in a pandas DataFrame format.
 

Functions:
- getAttributes(metadata): Extracts integer and specific string columns from metadata.
- getOnlySelectedData(ids, metadata): Filters metadata DataFrame based on selected IDs.
- getAge(ids, data): Retrieves age data for specified IDs from a scalar data DataFrame.
"""

import pandas as pd
import numpy as np
from icecream import ic



def getAttributes(metadata):
    """ 
    Gets column names from 'metadata' which are useable for attribute selection


    Args:
    - metadata (pd.DataFrame): The metadata DataFrame.

    returns:
    - int_columns (list): list of column names where the datatype is int64.
    - string_columns (list): list of column names 'Geschl' and 'Grobkategorie'

    Notes:
    - string_columns is for now hardcoded, so these need to be included in the metadata.csv
    """

    # Select integer columns
    int_columns = [col for col in metadata.columns if metadata[col].dtype == 'int64']

    # Select columns with specific names
    string_columns = [col for col in metadata.columns if col in ['Geschl', 'Grobkategorie']]

    unique_values = {col: metadata[col].unique().tolist() for col in string_columns}
   




    return int_columns, unique_values, string_columns


def getOnlySelectedData(ids, metadata):

    """
    Filters metadata DataFrame to include only rows with IDs in selected_ids and columns in int_columns.

    Args:
    - metadata (pd.DataFrame): The metadata DataFrame.
    - ids (List[int]): List of selected IDs.
    

    Returns:
    - filtered_data (pd.DataFrame): Filtered metadata DataFrame.
    """
    # Convert selected_ids to set for faster lookup
    selected_ids_set = set(ids)

    # get attribute name list from metadata
    int_attribute_names, _,  str_attribute_names = getAttributes(metadata)

    attribute_names = int_attribute_names + str_attribute_names
    # Filter rows: Keep only rows where 'DBId' matches one of the selected IDs
    filtered_rows = metadata[metadata['DBId'].isin(selected_ids_set)]

    # Filter columns: Keep only columns listed in int_columns
    filtered_data = filtered_rows[attribute_names]

    return filtered_data


def getAge(ids, data):

    """
    Filters metadata DataFrame to include only rows with IDs in selected_ids and columns in int_columns.

    Args:
    - ids (List[int]): List of selected IDs.
    - data (pd.DataFrame): The scalar DataFrame.


    Returns:
    - filtered_ages (list): List of ages of the visualized data.
    """

    selected_ids_set = set(ids)

    

    # Select the rows where Session_ID is in selected_ids_set
    selected_rows = data[data['Session_ID'].isin(selected_ids_set)]



    # If 'Age' is a column, retrieve its values for the selected rows
    filtered_ages = selected_rows['Age'].tolist()



    return filtered_ages


    



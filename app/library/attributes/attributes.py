import pandas as pd
from app.library.helpers.helpers import loadPickle


def getAttributes(metadata):
    """ 
    Gets column names from 'metadata' which are useable for attribute selection

    Parameters:
    metadata (pd.DataFrame): The metadata DataFrame.

    returns:
    int_columns (list): list of column names where the datatype is int64.
    unique_values (dict): dictionary where keys are column names and values are lists of unique values in those columns
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

    Parameters:
    metadata (pd.DataFrame): The metadata DataFrame.
    ids (List[int]): List of selected IDs.
    

    Returns:
    filtered_data (pd.DataFrame): Filtered metadata DataFrame.
    """
    # Convert selected_ids to set for faster lookup
    selected_ids_set = set(ids)

    #get attribute name list from metadata
    int_attribute_names, _, str_attribute_names = getAttributes(metadata)

    attribute_names = int_attribute_names + str_attribute_names
    # Filter rows: Keep only rows where 'DBId' matches one of the selected IDs
    filtered_rows = metadata[metadata['DBId'].isin(selected_ids_set)]

    # Filter columns: Keep only columns listed in int_columns
    filtered_data = filtered_rows[attribute_names]

    return filtered_data


def getAge():

    data,_,_ = loadPickle()

    



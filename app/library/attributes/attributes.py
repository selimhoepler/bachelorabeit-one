import pandas as pd
import numpy as np
from icecream import ic



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


def getAge(ids, data):

    selected_ids_set = set(ids)

    ic(data)

    # ic(data.iloc[:10, :5])

    # selected_rows = data.loc[data.index.get_level_values('Session_ID').isin(selected_ids_set)]


    # session_ids_values = selected_rows.index.get_level_values('Session_ID').tolist()

    # unique_top_level_columns = set(data.columns.get_level_values(0))

    # for col in unique_top_level_columns:
    #     ic(col)





    # ic(selected_rows)

    # filtered_ages = selected_rows.index.get_level_values('Age').tolist()

    # ic(filtered_ages)

     # Assuming Session_ID is in the first column (0)
    selected_rows = data[np.isin(data[:, 0], list(selected_ids_set))]
    
    ic(selected_rows[:10, :5])
    
    # Extracting the Session_ID values
    session_ids_values = selected_rows[:, 0].tolist()
    
    # As we can't get column names from a numpy array, we'll skip that part
    # Assuming Age is in the second column (1)
    filtered_ages = selected_rows[:, 1].tolist()
        

    
    ic(filtered_ages)




    return  filtered_ages 

    



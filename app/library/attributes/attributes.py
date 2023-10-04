import pandas as pd


def getAttributes(metadata):

    # Select integer columns
    int_columns = [col for col in metadata.columns if metadata[col].dtype == 'int64']

    # Further filter columns if necessary, based on domain knowledge or other criteria
    # selected_attributes = [col for col in int_columns if your_criteria(col)]

    return int_columns


def getOnlySelectedData(ids, metadata):

    """
    Filters metadata DataFrame to include only rows with IDs in selected_ids and columns in int_columns.

    Parameters:
    metadata (pd.DataFrame): The metadata DataFrame.
    ids (List[int]): List of selected IDs.
    

    Returns:
    pd.DataFrame: Filtered metadata DataFrame.
    """
    # Convert selected_ids to set for faster lookup
    selected_ids_set = set(ids)

    #get attribute name list from metadata
    attribute_names = getAttributes(metadata)

    # Filter rows: Keep only rows where 'DBId' matches one of the selected IDs
    filtered_rows = metadata[metadata['DBId'].isin(selected_ids_set)]

    # Filter columns: Keep only columns listed in int_columns
    filtered_data = filtered_rows[attribute_names]

    return filtered_data



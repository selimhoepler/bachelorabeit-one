import pandas as pd


def getAttributes(metadata):

    # Select integer columns
    int_columns = [col for col in metadata.columns if metadata[col].dtype == 'int64']

    # Further filter columns if necessary, based on domain knowledge or other criteria
    # selected_attributes = [col for col in int_columns if your_criteria(col)]

    return int_columns
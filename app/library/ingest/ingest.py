import pandas as pd
import numpy as np
# from app.library.data import prepare as prepare




def represents_int(s):
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

    scalar_data, array_data = load_matlab_csv(data_filename)
    array_data['Session_ID'] = scalar_data.loc[:, 'Session_ID']
    array_data = array_data.set_index('Session_ID')
    # create scalar and array df with index 'Session_ID'
    scalar_data = scalar_data.set_index('Session_ID', drop=False)

    meta_data, _ = load_matlab_csv(
        metadata_filename, scalar_and_array=False)
    meta_data = meta_data.set_index('DBid')
    # selecting only those metadata that are considered for UC1
    meta_data = meta_data.loc[scalar_data.index, :]

    #   Dies ist ein NumPy-Array, das die Information darüber speichert, ob die Daten für die rechte oder linke Seite (oder beide)
    #   des Patienten relevant sind. Diese Information wird aus den Spalten
    #   UC1_betroffen_RE und UC1_betroffen_LI in meta_data abgeleitet.

    side = np.ones(meta_data.UC1_betroffen_RE.shape[0])*(-1)
    side[meta_data.UC1_betroffen_LI == 1] = 0
    side[meta_data.UC1_betroffen_RE == 1] = 1
    side[
        (meta_data.UC1_betroffen_LI == 1) &
        (meta_data.UC1_betroffen_RE == 1)
    ] = 2

    print(f'[INFO] container.side length: {len(side)}')
    print(f'[INFO] container.data length: {len(array_data)}')
    print(f'[INFO] container.meta_data length: {len(meta_data)}')

    # attribute_values = meta_data.columns[429:]  # only select usable columns*
    # attribute_values = [
    #     col for col in meta_data[attribute_values]
    #     if represents_int(meta_data[col].values[0])
    # ]

    # print(attribute_values)

    # selected_attribute_values = [
    #     col for col in attribute_values[:20] if col in meta_data
    # ]

    # feature_table = prepare.prep_attribute(meta_data, selected_attribute_values)

    # print(feature_table)
    # print(meta_data)

    # csv_filename = 'beispiel.csv'

    # # DataFrame in die CSV-Datei schreiben
    # # feature_table.to_csv(csv_filename, index=False)

    # print(f'Daten wurden in die Datei "{csv_filename}" geschrieben.')

    # Die erste Zeile des DataFrames auswählen, um die Spaltennamen zu erhalten
    first_row = meta_data.iloc[0]

    # Spaltennamen, die auf "re" enden
    re_columns = [col for col in first_row.index if col.endswith('_re')]

    # Spaltennamen, die auf "li" enden
    li_columns = [col for col in first_row.index if col.endswith('_li')]

    # Alle anderen Spalten
    other_columns = [
        col for col in first_row.index if col not in re_columns and col not in li_columns]



    return array_data, meta_data, side


def save_data_to_file(data, filename):
    with open(filename, "w") as f:
        f.write(data.to_csv(index=False))
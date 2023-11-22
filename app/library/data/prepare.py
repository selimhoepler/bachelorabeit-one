"""
This module is designed for processing and preparing the GAIT data for analysis and visualization. 
It includes functions for preparing kinetic and kinematic data, handling affected data based on 
specified criteria, and creating a data structure for model execution. These functions will be executed after user selects 
the signals which he wants the models to be performed on. 
The function create_data_signalbase is called in signals.py.signal_data_selection, which is called in process_signals
at the route @signals 

Functions:
- prep_data: Prepares kinetic and kinematic data with optional subsampling and normalization.
- prepare_affected_data2: Prepares data for subjects with specific affected sides.
- create_data_signalbase: Extracts and organizes signals for model execution.
"""

import pandas as pd
from collections import defaultdict
import numpy as np
from icecream import ic


def prep_data(df, signals, columns, n=1, norm=None):
    """Prepare kinetic and kinematic data

    A dataframe df (e.g. provided by *load_matlab_csv*) contains kinetic
    and kinematic data. We can specify signals which we want to use
    and specific columns of these signals (e.g. medio-lateral or
    transversal direction). Furthermore, it can be specified if
    the time-series data should be subsampled (parameter n is the step size).
    This function is also used by the function *prepare_affected_data*.
    Parameter norm can be set to 'min-max' in order to
    perform a min-max normalization
    on each component.

    Warning: the columns are not python comform, as they start at 1!
    Returns: data
        data : DataFrame of requested signals and columns
    """


    data = pd.DataFrame()


    if len(signals) != len(columns):
        print('Error: Provide for each segnal a column array!')
        return

    for a, col in zip(signals, columns):

        # get only selected rows from array_data
        signals = df.loc[:, a]

            
        # loc gets rows (or columns) with particular labels from the index.
        # --> #temp = temp.loc[:,np.r_[1:102, 303:405, 505:607]].copy()
        # sind die columns immer 1:1212 benannt?

        # iloc gets rows (or columns) at particular positions in the index
        # (so it only takes integers)

        # cols = list(range(0,101))+list(range(303,404))+list(range(505,606))
        cols = []
        for c in col:

            cols = list(range(101*(c-1), 101*c, n))

            component = signals.iloc[:, cols].copy()



            if norm is not None:
                if norm == 'min-max':
                    component = (component - component.min().min()) / \
                                (component.max().max() - component.min().min())
                else:
                    print('Error: Provided normalization is not supported!')
            data = pd.concat([data, component], axis=1)

    return data






def prepare_affected_data2(df, signals, columns, side, n=1, norm=None):

    """Prepare affected data, so that for subjects with only one
    affected side the data for this specific side is provided and for
    subjects with both affected sides data for both legs is provided.

    A dataframe df (e.g. provided by *load_matlab_csv*) contains kinetic
    and kinematic data. We can specify signals which we want to use
    and specific columns of these signals (e.g. medio-lateral or
    transversal direction). This function is also used by the function
    *prepare_affected_data*. With the paramter side we specify which
    side is affected 0 - left, 1 - right and 2 - both. Parameter norm
    can be set to 'min-max' in order to perform a min-max normalization
    on each component.

    Returns: data
        left_affected_data : DataFrame of requested data from subjects with
        left affected extremity

        right_affected_data : DataFrame of requested data from subjects with
        right affected extremity

        both_affected_data : DataFrame of requested data from subjects with
        both affected extremities
    """

    left_affected_data = pd.DataFrame()
    right_affected_data = pd.DataFrame()
    both_affected_data = pd.DataFrame()



    for a, col in zip(signals, columns):
        attribute_side = a.split('_')[0]


        if attribute_side == 'L':

            #adding temp 2 times, as otherwise you cannot chose all patients when running the models,
            #does not change the data, just doubling dimensions
            temp = prep_data(df[side == 0], [a], [col], n, norm)
            left_affected_data = pd.concat(
                [left_affected_data, temp, temp],
                axis=1
                )
            
        elif attribute_side == 'R':

            temp = prep_data(df[side == 1], [a], [col], n, norm)
            right_affected_data = pd.concat(
                [right_affected_data, temp, temp],
                axis=1
                )
        else:
            print('Warning: Attribute names should start with L or R!')

        temp = prep_data(df[side == 2], [a], [col], n, norm)
        both_affected_data = pd.concat([both_affected_data, temp], axis=1)
    return left_affected_data, right_affected_data, both_affected_data


def create_data_signalbase(
        array_data,
        signals_dict: dict,
        side,
        n_list: list,
        pre_processing='euclidean',
        do_norm=None,
        legs='both'
        ) -> dict:
    """
    Extracts the signals at the given intervals from the raw input data.

    Args:

    array_data (DataFrame): Contains all gait data with all attributes.

    signals_dict (Dict): Dictionary containing the signals and columns
    for every signal name.

    side (List): List containing which collumn contains which side.

    n_list (List): List containing the intervals of the desired subsampling.

    do_norm (str): (Optional) Which normalization to use.

    Returns:
    Dictionary: containing the subsampled data for every interval passed in
    with n_list for all individual and combined affected sides.
    """
    print(f'[GENERATE][ENTER] create_data_signalbase()')
    data_dict = defaultdict(dict)

    for key in signals_dict:
        print(f'[INFO] key in signals_dict: \n{key}')
        print(f'[INFO] entire signals_dict: \n{signals_dict[key]}')
        
        data_dict[key] = {}
        labels = None
        left: pd.DataFrame
        right: pd.DataFrame
        both: pd.DataFrame
        ########################################
        ####################################
        #1: 
        ####################################
        ########################################
        left = pd.DataFrame()
        right = pd.DataFrame()
        both = pd.DataFrame()

        for x in n_list:
            




            if ('euclidean' in str(pre_processing).lower()):
           
                left, right, both = prepare_affected_data2(
                    array_data, 
                    signals_dict['signals'], 
                    signals_dict['columns'], 
                    side, 
                    n=x,
                    norm=do_norm)

            data_dict[key][str(x)] = {}
            data_dict[key][str(x)]['left_affected'] = left
            data_dict[key][str(x)]['right_affected'] = right
            data_dict[key][str(x)]['both_affected'] = both

            
        print(f'[GENERATE][EXIT] create_data_signalbase()')
        
    return data_dict, labels







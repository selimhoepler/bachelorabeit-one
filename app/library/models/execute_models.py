"""
This module contains functions for executing models on GAIT data. It is designed to run multiple models on preprocessed data,
handling different data selections and intervals. 
The module is used in the function execute_all_models from the route @execute.
It only runs ONE model at a time with ONE interval for this application

Functions:
- models_execute: Runs all models present in input_models on given data.
- execute: Executes all models provided for all intervals on the data.
"""

import datetime
import time
import pandas as pd
import numpy as np
from collections import defaultdict, Counter 


def models_execute(
        input_models: dict,
        data_in,
        identifier,
        selection,
        multivar_labels=None,
        do_print=False,
        ) -> dict:
    """
    Executes each model in the input_models dictionary on the provided data.

    Args:
    - input_models (dict): Dictionary containing models to be executed.
    - data_in (DataFrame): Data on which the models should be performed.
    - identifier (int): Interval identifier for model execution.
    - selection (str): Selection identifier used in model keys.
    - multivar_labels (list, optional): Labels for multivariate analysis. Defaults to None.
    - do_print (bool, optional): If True, prints debug information. Defaults to False.

    Returns:
    - dict: A dictionary containing the t-SNE data for all models, selections, and intervals.
    """

    print(f'[GENERATE][ENTER] models_execute() ({identifier})')
    models = {}
    model_keys = []
    for key in input_models:
        model_key = '{}_{}_{}'.format(selection, key, identifier)
        print(f'[INFO] Model key: {model_key}')
        if do_print:
            print(model_key)
        model = input_models[key]['model']
        models[model_key] = {'model': model}
        
        print(f'[INFO] executing model: {model}')
        print(f'[INFO] processing the following data: {data_in}')

        start_time = time.time()
        models[model_key]['tsne_data'] = model.fit_transform(data_in)  #tsne result data for visualization
        end_time = time.time()

        models[model_key]['time'] = end_time - start_time

        if multivar_labels is not None:
            models[model_key]['ids'] = multivar_labels
        else:
            models[model_key]['ids'] = data_in.index.values

        models[model_key]['tsne'] = pd.DataFrame(
            data=models[model_key]['tsne_data'],
            index=models[model_key]['ids'],
            columns=['dim1', 'dim2'])
        
        model_keys.append(model_key)
        print(f'[INFO] Model keys: {model_keys}')
    # print model timings
    if do_print:
        print('\nTimings:')
        for key in models:
            print('{}: {}'.format(
                key,
                str(datetime.timedelta(seconds=models[key]['time']))
                ))
        print('--------------------------')

    return models, model_keys


def execute(
        models,
        data_dict,
        interval_list,
        affected_side='both_affected',
        multivar_labels=None,
        do_print=False,
        leg='both'
        ) -> dict:
    """
    Executes all models provided by the 'models' dictionary for each interval in the 'interval_list'.

    Args:
    - models (dict): Contains all models generated for execution.
    - data_dict (dict): Contains preprocessed data organized by keys and intervals.
    - interval_list (list): List of intervals for subsampled data.
    - affected_side (str, optional): Specifies the affected side for analysis. Defaults to 'both_affected'.
    - multivar_labels (list, optional): Labels for multivariate analysis. Defaults to None.
    - do_print (bool, optional): If True, prints debug information. Defaults to False.
    - leg (str, optional): Specifies which leg data to consider ('both', 'individual', or 'all'). Defaults to 'both'.

    Returns:
    - dict: Dictionary containing the output for all models and intervals.
    """
        # Starting the execution process
    print(f'[GENERATE][ENTER] execute()')
    results = {}
    single_result = defaultdict(dict)
    model_key_list = []

    # Iterating over each key in the data dictionary
    for key in data_dict:
        print(f'[INFO] Key: {key}')
        # Iterating over each interval
        for interval in interval_list:
            print(f'[INFO] Interval: {interval}')  
            print(f'[INFO] Side dictionary:\n {data_dict[key][str(interval)]}') 
            print(f'[INFO] Type of data: {type(data_dict[key][str(interval)]["left_affected"])}')

            # Processing based on the 'leg' parameter
            if 'both' in leg:
                # Handling data wher only both legs are affected
                single_result, model_key = models_execute(
                    models,
                    data_dict[key][str(interval)]['both_affected'].dropna(),
                    '_{:02d}'.format(interval),
                    key,
                    do_print=False,
                    multivar_labels=multivar_labels
                )
                results.update(single_result)
                model_key_list.append(model_key)

            elif 'individual' in leg:
                # Handling data where only one side (left OR right) is affected
                print(f'INDIVIDUALLEG')
                print (f"length of left affected: {len(data_dict[key][str(interval)]['left_affected'])}")
                print (f"length of right affected: {len(data_dict[key][str(interval)]['right_affected'])}")
        
                single_result, model_key = models_execute(
                    models,
                    pd.concat([
                        data_dict[key][str(interval)]['left_affected'].dropna(),
                        data_dict[key][str(interval)]['right_affected'].dropna()
                    ]),
                    '_{:02d}'.format(interval),
                    key,
                    do_print=False,
                    multivar_labels=multivar_labels
                )
                results.update(single_result)
                model_key_list.append(model_key)

            else:
                # Handling allp patient data irrespective of the affected side
                print(f'ALL')
                print (f"length of left affected(dropna): {len(data_dict[key][str(interval)]['left_affected'].dropna())}")
                print (f"length of right affected(dropna): {len(data_dict[key][str(interval)]['right_affected'].dropna())}")
                print (f"length of both affected(dropna): {len(data_dict[key][str(interval)]['both_affected'].dropna())}")
                
                single_result, model_key = models_execute(
                    models,
                    pd.concat([
                        data_dict[key][str(interval)]['left_affected'].dropna(),
                        data_dict[key][str(interval)]['right_affected'].dropna(),
                        data_dict[key][str(interval)]['both_affected'].dropna()
                    ],
                    verify_integrity=True
                    ),
                    '_{:02d}'.format(interval),
                    key,
                    do_print=False,
                    multivar_labels=multivar_labels
                )
                results.update(single_result)
                model_key_list.append(model_key)
                
    print(f'[GENERATE][EXIT] execute()') 
    return results, model_key_list



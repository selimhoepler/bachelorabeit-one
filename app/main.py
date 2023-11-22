"""
This app processes GAIT data and displays the data with reduced dimensionality in a scatterplot.
The application uses FastAPI for handling web requests, allowing users to upload their data files and metadata.
Once the data is uploaded, users can select from various signal processing options and choose between t-SNE and UMAP models for visualization.
The app then processes the data accordingly and generates a scatterplot visualizing the reduced dimensionality data.

The application structure is divided into several modules:
- Ingestion: Handles the uploading and initial processing of data files.
- Helpers: Provides utility functions for data processing and file management.
- Signals: Manages signal data selection and preprocessing for model input.
- Attributes: Extracts and prepares attributes from the data for visualization.
- Models: Creates and manages t-SNE and UMAP models based on user settings.
- Execution: Executes the selected model and prepares the visualization data.

This app is designed for the purpose of a bachelor thesis, it includes code provided by Dipl.-Ing. Djordje Slijepčević.
It aims to be providing an easy-to-use interface for complex data processing and visualization tasks.

Created by: Selim Höpler
"""

# FastAPI imports
from fastapi import FastAPI, Request, File, UploadFile, Body
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# module imports from app files
from .library.ingest.ingest import *
from .library.helpers import helpers as helpers
from .library.signals.signals import signal_data_selection, create_checkboxes_signals
from .library.attributes.attributes import getAttributes, getOnlySelectedData, getAge
from .library.models import create_models, execute_models 

# other imports
import json
from pydantic import BaseModel
import tempfile
import logging

# initiating fastapi app
app = FastAPI()

# setting up templates and static files for fastapi
app.mount('/static', StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')

# setting up logging
logging.basicConfig(filename='app_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


#creating Tsne_Setting and UMAP_Setting as a pydantic BaseModel class
class TsneSettings(BaseModel):
    tsne_perplexity: int = 15
    tsne_iterations: int = 3000
    # tsne_seed: int = 1         # Dont think that should be customizable
    d_metric: str = "euclidean"

class UmapSettings(BaseModel):
    min_dist: float = 0.1
    n_neighbors: int = 15


class ExecuteModel(BaseModel):
    legs: str
    interval: int = 5



#route called on startup, displays page.html
@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    data = [{'hello':'world'}]  

    return templates.TemplateResponse('page.html', {'request': request, 'data': data})


@app.post("/ingest", description="Upload data and metadata CSV files, process them, and save the results for further analysis.")
async def upload_files(data_file: UploadFile = File(...), metadata_file: UploadFile = File(...)):

    """
    Receives data and metadata files from the user, saves them as temporary files,
    processes them to extract data, and saves the processed data in pickle format.
    
    Parameters:
    - data_file: UploadFile - The CSV file containing the data to be analyzed.
    - metadata_file: UploadFile - The CSV file containing metadata for the data file.
    
    Returns:
    - JSONResponse: A JSON response with a success or error message and status code.
    
    Raises:
    - HTTPException: An error with a status code indicating the type of failure.
    
    Notes:
    - Temporary files are created to handle the uploaded files.
    """



    try:
        data_content = await data_file.read()
        metadata_content = await metadata_file.read()

        # Create temp files for submitted data
        with tempfile.NamedTemporaryFile(delete=False) as data_tempfile, tempfile.NamedTemporaryFile(delete=False) as metadata_tempfile:
            data_tempfile.write(data_content)
            metadata_tempfile.write(metadata_content)
            data_tempfile_path = data_tempfile.name
            metadata_tempfile_path = metadata_tempfile.name
        
        # get filtered dataframes
        array_data, meta_data, side, scalar_data = get_datas(data_tempfile_path, metadata_tempfile_path)

        
        
        #save the data in pickle files
        try:
            helpers.savePickle(array_data, meta_data, side, scalar_data)
            message = "Data successfully saved"

            # TODO: delete temp files after everythings been done (?)

        except Exception as e:
            
            message = "Error while saving data"
            print(message, e)
        try:
            #signals and attributes for creating checkboxes in Frontend
            temp_checkboxes = create_checkboxes_signals(array_data)
            int_attributes, string_attributes, _ = getAttributes(meta_data)
            attributes = {'int_attributes': int_attributes, 'string_attributes': string_attributes}

        except Exception as e:
            message = "Error while accessing checkboxdata:"
            print(message, e)
            
            logging.exception(e)
        # send success message, signals, attributes to Frontend
        return JSONResponse(content={"response": {"message": message, 'checkboxes': temp_checkboxes, 'attributes': attributes}}, status_code=200)

    except Exception as e:
        print("Error while trying to read or filter data:")
        logging.exception(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/signals", description="Process selected signals from the uploaded data and save the results for model creation.")
async def process_signals(preset_data: dict):

    """
    This function gets called after submitting a preset, or selecting signals.
    Accepts a dictionary of preset data, loads saved dataframes, filters data based on selected signals, 
    and saves the filtered data for use in model creation.
    
    Parameters:
    - preset_data: dict - A dictionary containing user-selected signal processing presets.
    
    Returns:
    - JSONResponse: A JSON response with a success message and status code if processing is successful, 
                    or an error message and status code if an exception occurs.
    """



    try:
        
        print(f"this is selected preset as dict: {preset_data}")
        
        # loading previously saved dataframes
        try:
            array_data, _, side, _ = helpers.loadPickle()
        
        except Exception as e:
            print("Error while accessing data:", e)
            return JSONResponse(content={"error": str(e)}, status_code=500)
        
        # getting filtered data depending on selected signals, which the models will be used on
        try:

           signal_data = signal_data_selection(preset_data, array_data, side)

        
        except Exception as e:
            print("Error while loading signals:", e)
            logging.exception(e)
            return JSONResponse(content={"error": str(e)}, status_code=500)
        #print type of signal_data
        print(type(signal_data)) #dict


        
        # saving filtered data
        try:
            helpers.saveDict(signal_data, "signal_data")


        except Exception as e:
            print("Error while saving signals::", e)
            logging.exception(e)
            return JSONResponse(content={"error": str(e)}, status_code=500)


        # send success message to Frontend
        response_data = {"message": f"Signals have been successfully read!"}
        print(response_data)
        return JSONResponse(content=response_data, status_code=200)
    
    except ValueError as ve:
        logging.exception(ve)
        return JSONResponse(content={"error": str(ve)}, status_code=400)

    except Exception as e:
        logging.exception(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@app.post("/models", description="Create and save visualization models based on user settings.")
async def create_model(tsne_settings: TsneSettings, umap_settings: UmapSettings, selected_model_type: str = Body(...)):

    """
    Receives user-defined settings for t-SNE or UMAP models, creates the models accordingly, 
    and saves them for executing visualizations.
    
    Parameters:
    - tsne_settings: TsneSettings - Settings for t-SNE model creation.
    - umap_settings: UmapSettings - Settings for UMAP model creation.
    - selected_model_type: str - Identifier to select the model type to create.
    
    Returns:
    - JSONResponse: A JSON response with a message indicating successful model creation 
                    or an error message and status code if an exception occurs.
    """



    tsne_perplexity = tsne_settings.tsne_perplexity
    tsne_iterations = tsne_settings.tsne_iterations
    d_metric = tsne_settings.d_metric

    min_dist = umap_settings.min_dist
    n_neighbors = umap_settings.n_neighbors


    try:
        model_type = selected_model_type
        models = {}
       
       #create t-SNE or UMAP Model based on selection

        if model_type == "tsne":
            models = create_models.tsne(
                iter=tsne_iterations,
                begin_p=tsne_perplexity,
                end_p=tsne_perplexity + 1,
                step_p=1,
                # seed=tsne_seed,
                metric=str(d_metric).lower(),
            )
        elif model_type == "umap":
            models = create_models.umap(
                min_dist=min_dist,
                n_neighbors=n_neighbors,
                metric='euclidean',
                n_epochs=None
            )

        print( models)

        # saving models to be used later
        try:
            helpers.saveDict(models, "models")
        except Exception as e:
            print("Error while saving models:", e)
            logging.exception(e)
            return JSONResponse(content={"error": str(e)}, status_code=500)

        return JSONResponse(content={"message": "Modelle successfully created"}, status_code=200)
    except Exception as e:
        logging.exception(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)





@app.post("/execute", description="Execute all saved models with the current data and settings.")
async def execute_all_models(data: ExecuteModel):

    """
    Executes all saved models using the current data and user-defined settings for which leg is affected (both, individual, all patients).
    It returns the visualization data and saves relevant attributes for frontend access.
    
    Parameters:
    - data: ExecuteModel - A model containing user-defined settings for model execution.
    
    Returns:
    - JSONResponse: A JSON response with the visualization data if successful, 
                    or an error message and status code if an exception occurs.
    """



    selected_legs = data.legs
    interval = data.interval
    # rest of the code



    # Interval is a leftover from old experiments, is set to '5' here
    interval_list = list()
    interval_list.append(interval)

    try:
        # getting the needed files previously saved, 
        # models = t-SNE or UMPA model
        # signal_data = filtered data based on signal selection, where the model is being used on
        # metadata and scalar_data for extra information

        models = helpers.loadDict("models")
        signal_data = helpers.loadDict("signal_data")
        _,metadata ,_ ,scalar_data = helpers.loadPickle()
        

        tsne_results, model_keys = execute_models.execute(
        models,
        signal_data,
        interval_list,
        do_print=False,
        leg=selected_legs,
    )

        try:
            
            
            print(model_keys)
            # output_file_path = 'tsne_results.txt' # debugging

            # accessing relevant data from the saved dict
            model_name = list(tsne_results.keys())[0]
            print(f'[INFO] Results(keys)[0]: {list(tsne_results.keys())[0]}')

            signal_tsne_data = tsne_results[model_name]['tsne_data']  #get_clean_results from container

            # saving ids 
            data_ids = tsne_results[model_name]['ids']

            # x-coordinates of datapoints
            x_data = list(signal_tsne_data[:,0])

            # y-coordinates of datapoints
            y_data = list(signal_tsne_data[:,1])

            # z = the ids of the patient
            z_data = list(data_ids)

            # getting the age for every patient
            age_data = getAge(z_data, scalar_data)

            # preparing list for all patients with visualisation data, ids and age per patient 
            results = []
            for i in range(len(signal_tsne_data)):
                results.append({"x": x_data[i], "y": y_data[i], "z": z_data[i], "age": age_data[i]})


            # cleaning up possible NaN results
            results = helpers.replace_nan(results)
            print(f'[INFO] results: {results}')


            response_data = {"scatterplot_data": results}

            # getting only metadata from used patients
            filtered_data = getOnlySelectedData(z_data, metadata)

            
            # saving it in .json to access data from frontend
            helpers.saveJSON(filtered_data, "attributes.json")


            # getting results json ready
            json_str = json.dumps(response_data, cls=helpers.NumpyEncoder)



            # write_dict_to_text_file(tsne_results, output_file_path) #debugging

        except Exception as e:
            print("Error while preparing results:", e)
            logging.exception(e)
            return JSONResponse(content={"error": str(e)}, status_code=500)

        # if everything was successfull, sending data to Frontend
        return JSONResponse(content=json.loads(json_str), status_code=200)
    

    except ValueError as ve:
        logging.exception(ve)
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    except Exception as e:
        logging.exception(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
    


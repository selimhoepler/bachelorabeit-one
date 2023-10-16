

from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .library.ingest.ingest import *
import tempfile
from .library.helpers import helpers as helpers
from .library.signals.signals import signal_data_selection, create_checkboxes_signals
from .library.attributes.attributes import getAttributes, getOnlySelectedData
import logging
from .library.models import create_models, execute_models 
import pprint
from IPython.display import display as idisplay
import json
import numpy as np
from pydantic import BaseModel

app = FastAPI()

app.mount('/static', StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')

logging.basicConfig(filename='app_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


#creating Tsne_Setting and UMAP_Setting as a pydantic BaseModel class
class TsneSettings(BaseModel):
    tsne_perplexity: int = 15
    tsne_iterations: int = 3000
    # tsne_seed: int = 1         # Dont think that should be customizable
    d_metric: str = "euclidean"






@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    data = [{'hello':'world'}]  

    return templates.TemplateResponse('page.html', {'request': request, 'data': data})

@app.post("/ingest")
async def upload_files(data_file: UploadFile = File(...), metadata_file: UploadFile = File(...)):
    try:
        data_content = await data_file.read()
        metadata_content = await metadata_file.read()

        # Erstelle temporäre Dateien für den Inhalt der hochgeladenen Dateien
        with tempfile.NamedTemporaryFile(delete=False) as data_tempfile, tempfile.NamedTemporaryFile(delete=False) as metadata_tempfile:
            data_tempfile.write(data_content)
            metadata_tempfile.write(metadata_content)
            data_tempfile_path = data_tempfile.name
            metadata_tempfile_path = metadata_tempfile.name
        
        # Einlesen der Dateien mit load_matlab_csv
        array_data, meta_data, side = get_datas(data_tempfile_path, metadata_tempfile_path)
        
        # Hier kannst du die verarbeiteten Daten speichern oder verwenden
        
        #safe the data in pickle files
        try:
            helpers.savePickle(array_data, meta_data, side)
            message = "Daten erfolgreich eingelesen"

            # TODO: delete temp files after everythings been done (?)

        except Exception as e:
            print("Fehler beim Speichern der Daten:", e)
            message = "Fehler beim Speichern der Daten"

        try:
            temp_checkboxes = create_checkboxes_signals(array_data)
            int_attributes, string_attributes, _ = getAttributes(meta_data)
            attributes = {'int_attributes': int_attributes, 'string_attributes': string_attributes}
        except Exception as e:
            print("Fehler beim Erstellen der Checkboxen:", e)
            message = "Fehler beim Erstellen der Checkboxen"
            logging.exception(e)

        return JSONResponse(content={"response": {"message": message, 'checkboxes': temp_checkboxes, 'attributes': attributes}}, status_code=200)

    except Exception as e:
        print("Fehler beim Einlesen der Dateien:")
        exception_file_path = "exception.txt"  # Passe den Dateipfad an
        logging.exception(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/signals")
async def process_signals(preset_data: dict):  #OPTIONAL: Subsampling_rate: int, legs: str, pre_processing: str (Advanced Options)
    try:
        selected_preset = preset_data.get("preset")
        print(f"this is selected preset as dict: {preset_data}")
        
        try:
            array_data, meta_data, side = helpers.loadPickle()
        
        except Exception as e:
            print("Fehler beim Laden der Daten:", e)
            return JSONResponse(content={"error": str(e)}, status_code=500)
        
        try:
           # signal_data, signal_names = signal_data_selection(int(selected_preset), array_data, side)
           # trying with JSON Preset

           signal_data, signal_names = signal_data_selection(preset_data, array_data, side)
        
        except Exception as e:
            print("Fehler beim Laden der Signale:", e)
            logging.exception(e)
            return JSONResponse(content={"error": str(e)}, status_code=500)
        #print type of signal_data, signal_names
        print(type(signal_data)) #dict
        print(type(signal_names)) #list

        try:
            helpers.saveDict(signal_data, "signal_data")
            helpers.saveDict(signal_names, "signal_names")

        except Exception as e:
            print("Fehler beim Speichern der Signale:", e)
            logging.exception(e)
            return JSONResponse(content={"error": str(e)}, status_code=500)


        response_data = {"message": f"Die ausgewählte Option ist: {selected_preset}"}
        print(response_data)
        return JSONResponse(content=response_data, status_code=200)
    
    except ValueError as ve:
        return JSONResponse(content={"error": str(ve)}, status_code=400)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@app.post("/models")
async def create_model(tsne_settings: TsneSettings):
    tsne_perplexity = tsne_settings.tsne_perplexity
    tsne_iterations = tsne_settings.tsne_iterations
    # tsne_seed = tsne_settings.tsne_seed
    d_metric = tsne_settings.d_metric


    try:
        model_type = "tsne"
        models = {}
       

        if model_type == "tsne":
            models = create_models.tsne(
                iter=tsne_iterations,
                begin_p=tsne_perplexity,
                end_p=tsne_perplexity + 1,
                step_p=1,
                # seed=tsne_seed,
                metric=str(d_metric).lower(),
            )


        print(type(models))
        print( models)

        try:
            helpers.saveDict(models, "models")
        except Exception as e:
            print("Fehler beim Speichern der Modelle:", e)
            logging.exception(e)
            return JSONResponse(content={"error": str(e)}, status_code=500)

        return JSONResponse(content={"message": "Modelle wurden erstellt"}, status_code=200)
    except Exception as e:
        logging.exception(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/execute")
async def execute_all_models(    
    interval:int = 5
    ):

    interval_list = list()
    interval_list.append(interval)
    try:
        models = helpers.loadDict("models")
        signal_data = helpers.loadDict("signal_data")
        tsne_results, model_keys = execute_models.execute(
        models,
        signal_data,
        interval_list,
        do_print=True,
        leg="both",
    )

        try:
            helpers.saveDict(tsne_results, "tsne_results")
            print(type(tsne_results))
            print(model_keys)
            output_file_path = 'tsne_results.txt'

            model_name = list(tsne_results.keys())[0]
            print(f'[INFO] Results(keys)[0]: {list(tsne_results.keys())[0]}')

            signal_tsne_data = tsne_results[model_name]['tsne_data']  #get_clean_results from container

            data_ids = tsne_results[model_name]['ids']

            print(f'[INFO] signal_tsne_data: {signal_tsne_data}')

            x_data = list(signal_tsne_data[:,0])

            print(f'[INFO] x_data: {x_data}')

            y_data = list(signal_tsne_data[:,1])

            print(f'[INFO] y_data: {y_data}')

            z_data = list(data_ids)

            results = []
            for i in range(len(signal_tsne_data)):
                results.append({"x": x_data[i], "y": y_data[i], "z": z_data[i]})

            print(f'[INFO] results: {results}')

            response_data = {"scatterplot_data": results}




            _, metadata, _ = helpers.loadPickle()

            filtered_data = getOnlySelectedData(z_data, metadata)

            

            helpers.saveJSON(filtered_data)








            json_str = json.dumps(response_data, cls=helpers.NumpyEncoder)

            # jsonresults = results.tolist()





            





            write_dict_to_text_file(tsne_results, output_file_path) #debugging
        except Exception as e:
            print("Fehler beim Speichern der Modelle:", e)
            logging.exception(e)
            return JSONResponse(content={"error": str(e)}, status_code=500)

        return JSONResponse(content=json.loads(json_str), status_code=200)
    except Exception as e:
        logging.exception(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

def write_dict_to_text_file(data, file_path):
    with open(file_path, 'w') as txt_file:
        pp = pprint.PrettyPrinter(indent=4, stream=txt_file)
        pp.pprint(data)
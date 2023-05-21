"""
MAIN CODE FOR FINAL YEAR PROJECT BOTBUSTER
"""

# importing libraries
import json
import base64
from fastapi import FastAPI, HTTPException, Response, status 
from fastapi.middleware.cors import CORSMiddleware

# importing in-house code
from model.api import API
import model.datastructures as ds

# Initialising constants 
CONFIG_FILE_PATH = "config\config.json"
API_FILE_PATH = "config\\api.json"
RESULTS_FILE_PATH = "config\\results.json"

# set fastapi up
botbuster = FastAPI()

# set up fastapi to bypass CORS at the front end:
botbuster.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# writing endpoints
# calling apis to check the text
@botbuster.post("/checktext/") # endpoint #1 sending requests to the AI detection engines
def checkText(request: ds.checkText):
    list_of_apis = request.dict()["list_of_apis"]
    text = request.dict()["text"]
    full_results = {}
    with open(API_FILE_PATH, "r") as api_data_file:
        api_data = json.load(api_data_file)
        for api_option in list_of_apis:
            try:
                results = API(api_data[f"{api_option}"]).api_call(text)
                full_results[f"{api_option}"] = results
            except:
                full_results[f"{api_option}"] = "Error Detecting"
                continue
    path_to_general_score = {
        "GPTZero": 'GPTZero.documents.0.completely_generated_prob',
        "Writer": 'Writer.1.score',
        "Sapling AI": 'Sapling AI.score',
        "Hugging Face": 'Hugging Face.data.0.0.Fake'
    } 
    scores = {}
    for api in list_of_apis:
        path = path_to_general_score[api] 
        results = full_results
        for key in path.split('.'):
            try: 
                if key.isnumeric():
                    key = int(key)
                results = results[key]
                scores[f"{api}"] = int(results * 100)
            except KeyError:
                scores[f"{api}"] = "error getting score"     
            except:     
                scores[f"{api}"] = "unknown error"
    return scores

@botbuster.get("/getapis/")
async def getapis():
    api_info = {}
    try: 
        with open(API_FILE_PATH, "r") as api_data_file:
            api_data = json.load(api_data_file)
            for api in api_data.keys():
                api_info[f"{api}"] = []
    except:
        print("Internal Server Error", 500)
    else:
        for api in api_info.keys():
            try:
                api_info[f"{api}"].append(api.lower().replace(" ", "")) # sets this as a key for most html dynamic coding
                with open(CONFIG_FILE_PATH, "r") as config_data_file:
                    config_data = json.load(config_data_file)
                    api_logo_path = config_data["logos_base_path"] + config_data["logos"][f"{api}"] # sets file path for the system to open
                    with open(f"{api_logo_path}", "rb") as image:
                        api_info[f"{api}"].append(base64.b64encode(image.read()).decode("utf-8)")) # encodes the image in base 64 and decodes in utf-8
            except: # catches all errors and continues to the next api in the loop. If there is no logo etc, it will just not show up on UI
                continue
            else: # if no error, proceed to the next API in the loop
                continue
        return api_info

# adding apis to system
@botbuster.post("/addapi/")
def addApi(request: ds.addApi, response: Response):
    req = request.dict()
    try:
        API(req["api_details"])
        api_name = req["api_name"]
    except KeyError:
        raise HTTPException (status_code = 400, details = "missing details")
    else:
        with open(API_FILE_PATH, "r") as add_api_file:
            api_data = json.load(add_api_file)
            api_data[f"{api_name}"] = req["api_details"]
        with open(API_FILE_PATH, "w") as add_api_file:
            add_api_file.write(json.dumps(api_data, indent = 4))
            response.status_code = status.HTTP_204_NO_CONTENT

# load baseline APIs to api.json file
with open(CONFIG_FILE_PATH, "r") as config_file:
    config_data = json.load(config_file)
    with open(API_FILE_PATH, "w") as add_api_file:
        add_api_file.write(json.dumps(config_data["APIs"], indent = 4))



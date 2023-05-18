# importing libraries
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import base64
import asyncio 
import time
import js2py
import temp

# importing in-house code
from model.api import API

# Initialising constants 
CONFIG_FILE_PATH = "backend\config\config.json"
API_FILE_PATH = "backend\config\\apis.json"

# set flask up
app = Flask(__name__)

# set up flask to bypass CORS at the front end:
cors = CORS(app)

# writing endpoints
# calling apis to check the text
@app.route("/checktext/", methods=["POST"])
def checkText():
    ''' // async function
    start = time.time()
    req = request.get_json()
    list_of_apis = req["list_of_apis"]
    text = req["text"]
    full_results = {}

    async def call_api(api_option, config_data, text):
        results = await API(config_data["APIs"][f"{api_option}"]).api_call(text)
        return results

    with open(CONFIG_FILE_PATH, "r") as config_file:
        config_data = json.load(config_file)
        tasks = []
        for api_option in list_of_apis:
            tasks.append(call_api(api_option, config_data, text))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(asyncio.gather(*tasks))
        # results = await asyncio.gather(*tasks)
        for i, api_option in enumerate(list_of_apis):
            full_results[f"{api_option}"] = results[i]

    end = time.time()
    print(end - start)
    return jsonify(full_results)
    '''
    req = request.get_json()
    list_of_apis = req["list_of_apis"]
    text = req["text"]
    full_results = {}
    try: 
        with open(API_FILE_PATH, "r") as api_data_file:
            api_data = json.load(api_data_file)
            for api_option in list_of_apis:
                results = API(api_data[f"{api_option}"]).api_call(text)
                full_results[f"{api_option}"] = results
    except:
        print("Internal Server Error", 500)
        return Response(response="Internal Server Error", status = 500)
    else:
        return Response(response=json.dumps(full_results), status=200)

@app.route("/getapis/", methods = ["GET"])
def getapis():
    api_info = {}
    try: 
        with open(API_FILE_PATH, "r") as api_data_file:
            api_data = json.load(api_data_file)
            for api in api_data.keys():
                api_info[f"{api}"] = []
    except:
        print("Internal Server Error", 500)
        return Response(response="Internal Server Error", status = 500)
    else:
        for api in api_info.keys():
            try: 
                api_info[f"{api}"].append(api.lower().replace(" ", ""))
                with open(CONFIG_FILE_PATH, "r") as config_data_file:
                    config_data = json.load(config_data_file)
                    api_logo_path = config_data["logos"][f"{api}"]
                    with open(f"{api_logo_path}", "rb") as image:
                        api_info[f"{api}"].append(base64.b64encode(image.read()).decode("utf-8)"))
                        
            except:
                continue
            else: 
                continue
        return Response(response=json.dumps(api_info), status = 200)

# adding apis to system
@app.route("/addapi/", methods = ["POST"])
def addApi():
    req = request.get_json()
    try:
        API(req["api_details"])
        api_name = req["api_name"]
    except KeyError:
        return Response(response="missing details", status = 400)
    else:
        with open(API_FILE_PATH, "r") as add_api_file:
            api_data = json.load(add_api_file)
            api_data[f"{api_name}"] = req["api_details"]
        with open(API_FILE_PATH, "w") as add_api_file:
            add_api_file.write(json.dumps(api_data, indent = 4))
            return Response(status = 204)

#run the app
if __name__ == "__main__":
    # load baseline APIs to apis.json file
    with open(CONFIG_FILE_PATH, "r") as config_file:
        config_data = json.load(config_file)
        with open(API_FILE_PATH, "w") as add_api_file:
            add_api_file.write(json.dumps(config_data["APIs"], indent = 4))
    app.run("localhost", port = 6969, debug=True)


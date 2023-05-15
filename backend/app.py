# importing libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# importing in-house code
from model.api import API

# Initialising constants 
CONFIG_FILE_PATH = "backend\config\config.json"
ADD_API_FILE_PATH = "backend\config\\addapi.json"

# set flask up
app = Flask(__name__)

# set up flask to bypass CORS at the front end:
cors = CORS(app)

# writing endpoints
# calling apis to check the text
@app.route("/textarea", methods=["POST"])
def checkText():
    req = request.get_json()
    list_of_apis = req["list_of_apis"]
    text = req["text"]
    full_results = {}
    with open(CONFIG_FILE_PATH, "r") as config_file:
        config_data = json.load(config_file)
        for api_option in list_of_apis:
            print(api_option)
            object = API(config_data["APIs"][f"{api_option}"])
            results = object.api_call(text)
            full_results[f"{api_option}"] = results
    return jsonify(full_results)

# adding apis to system
@app.route("/addapi", methods = ["POST"])
def addApi():
    req = request.get_json()
    try:
        API({req["api_details"]})
        api_name = req["api_name"]
    except KeyError:
        return "missing details", 400
    except:
        return "Internal Server Error", 500
    else:
        with open(ADD_API_FILE_PATH, "w") as add_api_file:
            api_data = json.load(add_api_file)
            api_data[f"{api_name}"] = req["api_details"]
            return api_data

#run the app
if __name__ == "__main__":
    app.run(debug=True)
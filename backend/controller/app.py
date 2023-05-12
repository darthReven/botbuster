# importing librarys
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# importing in-house code
from ..model.api import API

# Initialising constants 
CONFIG_FILE_PATH = "backend\model\config.json"

# set flask up
app = Flask(__name__)

# set up flask to bypass CORS at the front end:
cors = CORS(app)

# writing endpoints
@app.route("/textarea", methods=["POST"])
def checkText():
    data = request.get_json()
    list_of_apis = data["list_of_apis"]
    text = data["text"]
    full_results = {}
    with open(CONFIG_FILE_PATH, "r") as config_file:
        config_data = json.load(config_file)
        for api_option in list_of_apis:
            print(api_option)
            object = API(config_data["APIs"][f"{api_option}"])
            results = object.api_call(text)
            full_results[f"{api_option}"] = results
    return jsonify(full_results)

@app.route("/addapi", methods = ["POST"])
def addApi():
    data = request.get_json()
    

#run the app
if __name__ == "__main__":
    app.run(debug=True)
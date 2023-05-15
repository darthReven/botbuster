import requests
import json

class API:
    def __init__(self, json):
        self.target = json["target"]
        self.header = json["headers"]
        self.body = json["body"]
        self.body_key = json["body_key"]

    #dynamic function for API calls
    def api_call(self, text):
        target = self.target
        headers = self.header
        body = self.body
        
        # add text to body
        body[f"{self.body_key}"] = text
        try:
            response = requests.post(target, headers = headers, json  = body)
            #if wrong/missing key, code runs - writer gives error
            #if wrong url, code runs - writer gives a "None"
            return response.json()
        except:
            pass

    def verify_add_api(self, json):
        pass

# TEST CODES

# with open("backend\model\config.json", "r") as config_file:
#     config_data = json.load(config_file)

#     API_names = config_data["APIs"]["API Names"]
#     pass
#     text = "hello this is a text to test the api call!"
#     object = API(config_data["APIs"]["Writer"])
#     results = object.api_call(text)
#     print(results)

    # for item in API_names:
    #     object = API(config_data["APIs"][f"{item}"])
    #     results = object.api_call(text)
    #     print(results)
import requests

class API:
    def __init__(self, json: dict):
        self.target = json["target"]
        self.header = json["headers"]
        self.body = json["body"]
        self.body_key = json["body_key"]
        self.data_type = json["data_type"]

    #dynamic function for API calls
    def api_call(self, text: str):        
        # add text to body
        if self.data_type == "string":
            self.body[f"{self.body_key}"] = text
        elif self.data_type == "list":
            self.body[f"{self.body_key}"] = [text]
        try:
            response = requests.post(self.target, headers = self.header, json  = self.body)
            #if wrong/missing key, code runs - writer gives error
            #if wrong url, code runs - writer gives a "None"
        except:
            return "Internal Server Error", 500
        else:
            return response.json()

    def api_check(self):
        pass 

    @classmethod
    async def api_body_check(api):
        pass

    @classmethod
    async def api_target_check(api):
        #direct to virus total/phishing api

        pass
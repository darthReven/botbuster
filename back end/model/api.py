import requests
import json

class API:
    def __init__(self, json):
        self.target = json["target"]
        self.api_key = json["api_key"]
        self.header = json["headers"]
        self.body = json["body"]
        self.body_key = json["body_key"]
        
    '''
        # GPTzero API key & url
        self.GPTzero_api_key = api_key
        self.GPTzero_url = "https://api.gptzero.me/v2/predict/text"

        # writer API key & url
        self.writer_api_key = "OvHYORkICMve9i5mqxlOcEc8hZdLlFBqoR2PRjlsdwQDWmqPhFXKmojbgecpy0UoeD18kksoAHum54zU6c4PR7-HLfSUOrXu1wW4cKV0L3ZrzWFQDS5JdH1lE4flCFDK"
        self.writer_url = "https://enterprise-api.writer.com/content/organization/520409/detect"

        # sapling AI API key & url
        self.saplingai_api_key = "OY3XCOUYGA9HF0DVR9WDZMDKFIQ2C86N"
        self.saplingai_url = "https://api.sapling.ai/api/v1/aidetect"
    '''
    #dynamic function for API calls
    def api_call(self, text):
        target = self.target
        headers = self.header
        body = self.body
        
        # add text to body
        body[f"{self.body_key}"] = text

        response = requests.post(target, headers = headers, json  = body)
        return response.json()

    '''
    # GPTzero
    def gptzero(self, text):
        url = f'{self.GPTzero_url}/text'
        headers = {
            "accept": "application/json",
            "X-Api-Key": self.GPTzero_api_key,
            "Content-Type": 'application/json'
        }
        body = {
            "document": text # where the text should be
        }
        response = requests.post(url, headers = headers, json = body)
        return response.json()

    # Writer
    def writer(self, text) :
        url = self.writer_url
        headers = {
            "accept": "application/json",
            "Authorization": self.writer_api_key,
            "content-type": "application/json"
        }
        body = {
            "input": text
        }
        response = requests.post(url, headers = headers, json = body)
        return response.json()

    # Sapling AI
    def sapling_ai(self, text):
        url = "https://api.sapling.ai/api/v1/aidetect"
        headers = {}
        body = {
            "key": "OY3XCOUYGA9HF0DVR9WDZMDKFIQ2C86N",
            "text": "hello this is a text to test the api call!",
            "sent_scores": True
        }
        response = requests.post(url, headers = headers, json = body)
        print(response.text)
        return response.json 
    '''

with open("back end\model\config.json", "r") as config_file:
    config_data = json.load(config_file)

    API_names = config_data["APIs"]["API Names"]

    text = "hello this is a text to test the api call!"

    for item in API_names:
        object = API(config_data["APIs"][f"{item}"])
        results = object.api_call(text)
        print(results)

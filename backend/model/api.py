'''
AY2023/24 Final Year Project 
DISM3A68

p2104092 Lucas Quek
p2104104 Elliot Ang
p2128511 Kara Huang
p2128649 Cheong Yue Ming
P2128962 Sibi Srinivas S/O Ganesan
'''

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
            self.body[self.body_key] = text
        elif self.data_type == "list":
            self.body[self.body_key] = [text]
        try:
            response = requests.post(self.target, headers = self.header, json  = self.body)
            #if wrong/missing key, code runs - writer gives error
            #if wrong url, code runs - writer gives a "None"
            # assert response.code == 200
        except:
            return "Internal Server Error", 500
        else:
            return response.json()
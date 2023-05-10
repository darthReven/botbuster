# GPTzero functions coded with reference to https://github.com/Haste171/gptzero

import os
import requests

class API:
    def __init__(self, api_key):
        # GPTzero API key & url
        self.GPTzero_api_key = api_key
        self.GPTzero_url = "https://api.gptzero.me/v2/predict"

        # writer API key & url
        self.writer_api_key = "OvHYORkICMve9i5mqxlOcEc8hZdLlFBqoR2PRjlsdwQDWmqPhFXKmojbgecpy0UoeD18kksoAHum54zU6c4PR7-HLfSUOrXu1wW4cKV0L3ZrzWFQDS5JdH1lE4flCFDK"
        self.writer_url = "https://enterprise-api.writer.com/content/organization/520409/detect"

        # sapling AI API key & url
        self.saplingai_api_key = "OY3XCOUYGA9HF0DVR9WDZMDKFIQ2C86N"
        self.saplingai_url = "https://api.sapling.ai/api/v1/aidetect"

    # GPTzero
    def text_predict(self, text):
        url = f'{self.GPTzero_url}/text'
        headers = {
            'accept': 'application/json',
            'X-Api-Key': self.GPTzero_api_key,
            'Content-Type': 'application/json'
        }
        body = {
            'document': text # where the text should be
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
        payload = {
            "key": self.saplingai_api_key,
            "text": text,
            "sent_scores": True
        }
        response = requests.post(url, json = payload)
        print(response.text)

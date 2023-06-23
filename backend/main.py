"""
MAIN CODE FOR FINAL YEAR PROJECT BOTBUSTER

install uvicorn, fastapi

in command prompt, run "uvicorn main:botbuster --reload"

libaries needed:
uvicorn
fastapi
asyncio
pyppeteer
re
json
base64
"""

# importing libraries
import json
import base64
from fastapi import FastAPI, HTTPException, Response, status 
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import pyppeteer
import textract
from PyPDF2 import PdfFileReader
from flask import request, jsonify

# importing in-house code
from model.api import API
import model.datastructures as ds
import model.socialMediaScraper as sms

# Initialising constants 
CONFIG_FILE_PATH = "config\config.json"
API_FILE_PATH = "config\\apis.json"
RESULTS_FILE_PATH = "config\\result.json"

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
    with open(CONFIG_FILE_PATH, "r") as config_data_file:
        config_data = json.load(config_data_file)
    with open(API_FILE_PATH, "r") as api_data_file:
        api_data = json.load(api_data_file)
        for api_option in list_of_apis:
            try:
                results = API(api_data[f"{api_option}"]).api_call(text)
                full_results[f"{api_option}"] = results
            except:
                full_results[f"{api_option}"] = "Error Detecting"
                continue
    scores = {
        "general_score": {},
        "sentence_score": []
    }
    for sentence in text.split("."):
        sentence =  sentence.strip() + "."
        if sentence == ".":
            continue
        scores["sentence_score"].append({f"{sentence}": {"highlight": 0, "api": []}})
    for api in list_of_apis: 
        # checking for general score 
        path = config_data["path_to_general_score"][api] 
        results = full_results 
        for key in path.split('.'):
            try: 
                if key.isnumeric():
                    key = int(key)
                results = results[key]
                scores["general_score"][f"{api}"] = int(results * 100)
            except KeyError:
                scores["general_score"][f"{api}"] = "error getting score"     
            except:     
                scores["general_score"][f"{api}"] = "unknown error"
        # checking for sentence score
        try:
            path1 = config_data["path_to_sentence_score"][api][0]
            path2 = config_data["path_to_sentence_score"][api][1]
        except KeyError:
            continue
        else:
            results = full_results # checking for sentence score
            for key in path1.split("."):
                try:
                    if key.isnumeric():
                        key = int(key)
                    results = results[key]
                except KeyError:
                    break
            for num in range(0, len(results)):
                try: 
                    for key in scores["sentence_score"][num].keys():
                        if key == results[num]["sentence"] and results[num][path2] > 0.70:
                            scores["sentence_score"][num][key]["api"].append(api)
                            scores["sentence_score"][num][key]["highlight"] += 1/len(list_of_apis)
                except:
                    break
            with open("config\\result.json", "w") as score_file:
                score_file.write(json.dumps(full_results, indent = 4))
            with open("config\scores.json", "w") as score_file:
                score_file.write(json.dumps(scores, indent = 4))
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

# getting webscraper data
@botbuster.get("/webscraper/")
def webScraping():
    async def scraper(website, pageurl):
        browser = await pyppeteer.launch(
            headless=False,
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False
        )
        page = await browser.newPage()
        await page.goto(pageurl)

        items = await sms.scrapeInfiniteScrollItems(page, sms.websiteConfigs[website], 5)
        uniqueItems = []
        seenItems = set()
        for item in items:
            itemTuple = tuple(item)
            if itemTuple not in seenItems:
                uniqueItems.append(item)
                seenItems.add(itemTuple)

        # print(items)
        # for item in uniqueItems:
        #     print("Selector:", item[0])
        #     print("Element:", item[1])
        #     print()
        
        await browser.close()
        return uniqueItems
    
    def callSMS(pageurl):
        website = sms.identifyURL(pageurl)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        items1 = loop.run_until_complete(scraper(website, pageurl))
        return items1
    
    def checkURL(pageurl):
        #put in the check url function to call the appropriate scraper e.g. social media scraper, forum scraper or generic scraper
        print()

    pageurl = "https://twitter.com/nasa"
    items=callSMS(pageurl)
    return items
    
        
#extracting text from user's file
@botbuster.post("/extract")
def extract_text():
    print('api has been called')
    file = request.files['file']
    file_extension = file.filename.rsplit('.', 1)[1].lower()

    if file_extension == 'docx':
        text = textract.process(file, method='python').decode('utf-8')
        print(text)
    elif file_extension == 'pdf':
        reader = PdfFileReader(file)
        text = ""
        for page in range(reader.getNumPages()):
            text += reader.getPage(page).extract_text()
    elif file_extension == 'txt':
        text = file.read().decode('utf-8')
    else:
        return jsonify({'error': 'Unsupported file format'})
    return jsonify({'text': text})

# load baseline APIs to api.json file
with open(CONFIG_FILE_PATH, "r") as config_file:
    config_data = json.load(config_file)
    with open(API_FILE_PATH, "w") as add_api_file:
        add_api_file.write(json.dumps(config_data["APIs"], indent = 4))



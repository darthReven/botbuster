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
python-multipart ** for form data (even though not imported)
"""

# importing libraries
from fastapi import FastAPI, HTTPException, Response, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from urllib.parse import urlparse
from PIL import Image
import json
import base64
import asyncio
import textract
import os
import pytesseract
import cv2
import numpy as np

# importing in-house code
from model.api import API
import model.datastructures as ds
import model.socialMediaScraper as sms
import model.genericWebScraper as gws
import model.webScrapers as ws

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
            print(api_option)
            try:
                results = API(api_data["AIGCD APIs"][f"{api_option}"]).api_call(text)
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
            # with open("config\\result.json", "w") as score_file:
            #     score_file.write(json.dumps(full_results, indent = 4))
            # with open("config\scores.json", "w") as score_file:
            #     score_file.write(json.dumps(scores, indent = 4))
            print(scores)
    return scores

@botbuster.get("/getapis/")
async def getapis():
    api_info = {}
    try: 
        with open(API_FILE_PATH, "r") as api_data_file:
            api_data = json.load(api_data_file)
            for api_category in api_data.keys():
                api_info[f"{api_category}"] = {}
                for api in api_data[f"{api_category}"].keys():
                    api_info[f"{api_category}"][f"{api}"] = []
    except:
        print("Internal Server Error", 500)
    else:
        for api_category in api_info.keys(): 
            for api in api_info[f"{api_category}"]:
                try:
                    api_info[f"{api_category}"][f"{api}"].append(api.lower().replace(" ", "")) # sets this as a key for most html dynamic coding
                    with open(CONFIG_FILE_PATH, "r") as config_data_file:
                        config_data = json.load(config_data_file)
                        api_logo_path = config_data["logos_base_path"] + config_data["logos"][f"{api}"] # sets file path for the system to open
                        with open(f"{api_logo_path}", "rb") as image:
                            api_info[f"{api_category}"][f"{api}"].append(base64.b64encode(image.read()).decode("utf-8)")) # encodes the image in base 64 and decodes in utf-8
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
        raise HTTPException (status_code = 400, detail = "missing details")
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
    with open(CONFIG_FILE_PATH, "r") as config_data_file:
        websiteConfigs = json.load(config_data_file)["website_configs"]
    # pageurl = "https://theindependent.sg/news/singapore-news/"
    pageurl = "https://www.reddit.com/r/nasa/comments/14cna63/reddit_inc_is_intentionally_killing_off_3rdparty/"
    # pageurl = "https://twitter.com/nasa"
    # pageurl = "https://docs.python.org/3/library/urllib.parse.html"
    websiteName = urlparse(pageurl).netloc #getting the website name from the url
    print(websiteName)
    scrapingData = websiteConfigs.get(f"{websiteName}", websiteConfigs["default"])

    if scrapingData["func"] == "sms": # calling the social media scraper
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        items = loop.run_until_complete(ws.scraper(scrapingData["elements"], pageurl))
        print(items)
    elif scrapingData["func"] == "gws": # calling the generic web scraper
        items = ws.genericScraper(scrapingData["elements"], pageurl)
        print(items)
    else: 
        raise HTTPException (status_code = 500, detail = "Internal Server Error")
    return items
        
#extracting text from user's file
@botbuster.post("/extract")
def extract_text(file: UploadFile):
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    print(file.filename)
    contents = file.file.read()
    with open(f"temp.{file_extension}", 'wb') as f:
        f.write(contents)
    image = np.array(Image.open(f"temp.{file_extension}"))
    normalised_image = np.zeros((image.shape[0], image.shape[1]))
    image = cv2.normalize(image, normalised_image, 0, 255, cv2.NORM_MINMAX)
    image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)[1]
    image = cv2.GaussianBlur(image, (1, 1), 0)
    text = pytesseract.image_to_string(image)
    try: 
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        print(file.filename)
        contents = file.file.read()
        with open(f"temp.{file_extension}", 'wb') as f:
            f.write(contents)
        if file_extension == 'docx':
            text = textract.process(f"temp.{file_extension}", method = "python").decode('utf-8')
        elif file_extension == 'pdf':
            reader = PdfReader(f"temp.{file_extension}") # creating a pdf reader object
            text = ""
            for page_num in range (0, len(reader.pages)):
                print(f'test {page_num} of {len(reader.pages)}')
                page = reader.pages[page_num] # getting a specific page from the pdf file
                page_content = page.extract_text() # extracting text from page
                text += f"{page_content} \n"
            for page in range(reader.getNumPages()):
                text += reader.getPage(page).extract_text()
        elif file_extension == 'txt':
            text = textract.process(f"temp.{file_extension}", method = "python").decode('utf-8')
        else:
            print('unsupported')
            return HTTPException(status_code = 400, detail = "Unsupported File Type")
    except:
        raise HTTPException(status_code = 500, detail = "Internal Server Error")
    finally:
        os.remove(f"temp.{file_extension}")
    return text


# load baseline APIs to api.json file
with open(CONFIG_FILE_PATH, "r") as config_file:
    config_data = json.load(config_file)
    with open(API_FILE_PATH, "w") as add_api_file:
        add_api_file.write(json.dumps(config_data["APIs"], indent = 4))
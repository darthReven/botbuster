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
from fastapi import FastAPI, HTTPException, Response, status, UploadFile
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
import time

# importing in-house code
from model.api import API
import model.data_structures as ds
# import model.social_media_scraper as sms
# import model.generic_web_scraper as gws
import model.web_scrapers as ws
import model.graph as graph
import model.text as text_utils

# Initialising constants 
# setting file paths for configuration files
CONFIG_FILE_PATH = r"config\config.json"
API_FILE_PATH = r"config\api.json"
RESULTS_FILE_PATH = r"config\result.json"
# setting file path to tesseract
pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"

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
def check_text(request: ds.check_text):
    start = time.perf_counter()
    list_of_apis = request.dict()["list_of_apis"]
    text = request.dict()["text"]
    full_results = {} # create dictionary to store all results
    scores = { # create dictionary to store all scores
        "general_score": {api_category : {} for api, api_category in list_of_apis}, # dictionary comprehension to have a nested dictionary to store each category of APIs and overall score for each API
        "sentence_score": []  # keeping a score for each sentence   
    }
    total_score = {} # store score of each API before taking the average
    with open(CONFIG_FILE_PATH, "r") as config_data_file: # load in config data from config file
        config_data = json.load(config_data_file)
    with open(API_FILE_PATH, "r") as api_data_file: # load in API data from api file
        api_data = json.load(api_data_file)
    # change this to the text chunking functions
    list_of_texts = text_utils.chunk(text, config_data["chunk_option"])
    print("list of texts")
    print(list_of_texts)
    '''
    for sentence in text.split("."):
        sentence =  sentence.strip() + "."
        if sentence == ".":
            continue
        scores["sentence_score"].append({f"{sentence}": {"highlight": 0, "api": []}})
    '''
    
    for api, api_category in list_of_apis: # loop through all APIs
        total_score[f"{api_category}"] = {
            "score": 0,
            "num_apis": 0,
        }
        try:
            full_results[f"{api}"] = {}
            for num, text in enumerate(list_of_texts):
                for sentence in text_utils.chunk_by_sentences(text[0]):
                    scores["sentence_score"].append({f"{sentence}": {"highlight": 0, "api": []}})
                results = API(api_data[f"{api_category}"][f"{api}"]).api_call(text[0])
                full_results[f"{api}"][num] = results
        except Exception:
            full_results[f"{api}"] = "Error Detecting"
            continue
        try:
            # checking for general score 
            path = config_data["path_to_general_score"][api] # get the path
            results = full_results # set the results to loop through
            for key in path.split('.'): # loop through each key in the path to general score
                if key.isnumeric(): # if the key is numerical, convert it to an int
                    key = int(key)
                try: 
                    results = results[key] # try to path to the score
                    scores["general_score"][f"{api_category}"][f"{api}"] = round(float(results) * 100,1) # appends general score to the dictionary
                    total_score[f"{api_category}"]["score"] += round(float(results) * 100,1) # sums the general scores of all apis
                    total_score[f"{api_category}"]["num_apis"] += 1 # sums the number of APIs in the category
                    final_score = total_score[f"{api_category}"]["score"]/total_score[f"{api_category}"]["num_apis"] # gets the average score of all the APIs in each category
                    scores["general_score"][f"{api_category}"]["overall_score"] = round(final_score,1) # appends the average score
                except TypeError: # Type error will occur if the loop hasn't reached the score
                    continue  # continue to the next key in the loop
                except KeyError: # If there is an error with the path
                    scores["general_score"][f"{api_category}"][f"{api}"] = "error getting score" 
                except Exception: # catch all other errors
                    continue
            # checking for sentence score
            try:
                path1 = config_data["path_to_sentence_score"][api][0] # path to the list of the sentences
                path2 = config_data["path_to_sentence_score"][api][1] # path to the score of each sentence
            except KeyError: # Key Error will trigger is there is no path to sentence score (API does not have this capability)
                continue
            else:
                results = full_results # checking for sentence score
                for key in path1.split("."): # loops through each key in the path to sentence scores
                    try:
                        if key.isnumeric(): # if the key is numerical, convert it to an int
                            key = int(key)
                        results = results[key] # try to path to the score
                    except KeyError or TypeError or Exception:
                        break
                for num in range(0, len(results)): # loop through each sentence of results
                    try: 
                        for key in scores["sentence_score"][num].keys():
                            # if key == results[num]["sentence"] and results[num][path2] > 0.70: # if score above > 70%, add the  highlight and the api name ## commented this out because each sentence doesn't match yet
                            if results[num][path2] > 0.70: # if score above > 70%, add the  highlight and the api name
                                scores["sentence_score"][num][key]["api"].append(api)
                                scores["sentence_score"][num][key]["highlight"] += 1/len(total_score[f"{api_category}"]["num_apis"])
                    except:
                        break
        except:
            continue
    with open(RESULTS_FILE_PATH, "w") as results_file: # load in API data from api file
        results_file.write(json.dumps(full_results, indent=4))
    # graph.generate_graph(scores["general_score"]) # generate the graph with the general scores of each API
    end = time.perf_counter()
    print(end - start)
    return scores

@botbuster.get("/getapis/") # endpoint #2 retrieving available API information
async def get_apis():
    api_info = {} 
    try: 
        with open(API_FILE_PATH, "r") as api_data_file:
            api_data = json.load(api_data_file) # grabs all API data from API config file
            for api_category in api_data.keys(): # loops through the API categories
                api_info[f"{api_category}"] = {} # creates an empty dictionary for each category
                
                for api in api_data[f"{api_category}"].keys(): # loops through all API in each category 
                    api_info[f"{api_category}"][f"{api}"] = [api.lower().replace(" ", "")] # creates 
                    try: 
                        with open(CONFIG_FILE_PATH, "r") as config_data_file:
                            config_data = json.load(config_data_file)
                            api_logo_path = config_data["logos_base_path"] + config_data["logos"][f"{api}"] # sets file path for the system to open
                            with open(f"{api_logo_path}", "rb") as image:
                                api_info[f"{api_category}"][f"{api}"].append(base64.b64encode(image.read()).decode("utf-8)")) # encodes the image in base 64 and decodes in utf-8
                    except Exception: 
                        continue # catches all errors and continues to the next api in the loop. If there is no logo etc, it will just not show up on UI
    except Exception:
        raise HTTPException (status_code = 500, detail = "Internal Server Error")
    return api_info

# adding apis to system
@botbuster.post("/addapi/") # endpoint #3 adding APIs to the system
def add_api(request: ds.add_api, response: Response):
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
@botbuster.post("/webscraper/") # endpoint #4 scraping data from websites
def web_scraping(request: ds.web_scraper):
    page_url = request.dict()["page_url"]
    with open(CONFIG_FILE_PATH, "r") as config_data_file: # opens configuration settings to be used to decide which elements to scrape
        website_configs = json.load(config_data_file)["website_configs"]
    website_name = urlparse(page_url).netloc # getting the website name from the url
    scraping_data = website_configs.get(f"{website_name}", website_configs["default"]) # extract the proper elements to scrape from the website, if website not in database, use default elements
    if scraping_data["func"] == "sms": # calling the social media scraper
        loop = asyncio.new_event_loop() # creates a new event loop and 
        asyncio.set_event_loop(loop) # set created loop as the active one
        items = loop.run_until_complete(ws.scraper(scraping_data["elements"], page_url))
    elif scraping_data["func"] == "gws": # calling the generic web scraper
        items = ws.genericScraper(scraping_data["elements"], page_url)
    else: 
        raise HTTPException (status_code = 500, detail = "Internal Server Error")
    return items
        
# extracting text from user's file
@botbuster.post("/extract/") # endpoint #4 scraping data from files
def extract_text(file: UploadFile):
    try: 
        file_extension = file.filename.rsplit('.', 1)[1].lower() #extracts file extension from file name
        contents = file.file.read() # gets content of file out in bytes
        with open(f"temp.{file_extension}", 'wb') as f:
            f.write(contents) # writes a temporary file with the same bytes
        if file_extension == 'docx': # if it's docx file
            text = textract.process(f"temp.{file_extension}", method = "python").decode('utf-8')
        elif file_extension == 'txt':  # if it's txt file
            text = textract.process(f"temp.{file_extension}", method = "python").decode('utf-8')
        elif file_extension == 'pdf': # if it's pdf file
            reader = PdfReader(f"temp.{file_extension}") # creating a pdf reader object
            text = ""
            for page_num in range (0, len(reader.pages)):
                page = reader.pages[page_num] # getting a specific page from the pdf file
                page_content = page.extract_text() # extracting text from page
                text += f"{page_content} \n"
        elif file_extension == "jpg": # if it's image files
            image = np.array(Image.open(f"temp.{file_extension}")) # create image
            normalised_image = np.zeros((image.shape[0], image.shape[1]))
            # remove distractions in the photo using cv
            image = cv2.normalize(image, normalised_image, 0, 255, cv2.NORM_MINMAX)
            image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)[1]
            image = cv2.GaussianBlur(image, (1, 1), 0)

            text = pytesseract.image_to_string(image) # use pytesseract to extract text
        else:
            return HTTPException(status_code = 400, detail = "Unsupported File Type")
    except:
        raise HTTPException(status_code = 500, detail = "Internal Server Error")
    finally:
        os.remove(f"temp.{file_extension}") # delete the temporary file whether there was an error or not
    return text

# # getting graph data
# @botbuster.post("/graph/")
# def web_scraping(request: ds.gen_graph):
#     general_score = request.dict()["general_score"]
#     sentence_score = request.dict()["sentence_score"]
#     graph.generate_graph(general_score)

# load baseline APIs to api.json file
with open(CONFIG_FILE_PATH, "r") as config_file:
    config_data = json.load(config_file)
    with open(API_FILE_PATH, "w") as add_api_file:
        add_api_file.write(json.dumps(config_data["APIs"], indent = 4))
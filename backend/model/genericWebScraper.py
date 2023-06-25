import requests
from bs4 import BeautifulSoup
import sys
from fastapi import HTTPException

sys.stdout.reconfigure(encoding='utf-8') #so that other languages can be printed

def scraper(listOfElements: list, pageurl):
    response = requests.get(pageurl)
    if response.status_code == 200: 
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        raise HTTPException(status_code = 400, detail = "Target website could not be scraped due to errors on that website, please check the URL again.")
    extractedText = []
    for element in listOfElements:
        if "." in element:
            splitElement = element.split(".", 1)
            elementType = splitElement[0]
            elementClass = splitElement[1]
            elements = soup.find_all(elementType, class_= elementClass)
            for element in elements:
                text = element.get_text(strip=True)
                extractedText.append([elementType, text]) 
        else:
            elementType = element
            elements = soup.find_all(elementType)
            for element in elements:
                text = element.get_text(strip=True)
                extractedText.append([elementType, text]) 
    return extractedText
'''

'''
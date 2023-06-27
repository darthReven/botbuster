# social media scraper moduels
import asyncio
import pyppeteer
# generic webscraper modules
import requests
from bs4 import BeautifulSoup
import sys
from fastapi import HTTPException

# social media scraper
async def scrapeInfiniteScrollItems(page, contentSelector, itemTargetCount):
    await asyncio.sleep(2.5)
    items = []

    while itemTargetCount > len(items):
        selectedItems = await page.evaluate('''(contentselector) => {
            const selectedItems = [];
            const elements = Array.from(document.querySelectorAll("*"));

            for (const element of elements) {
                for (const selector of contentselector) {
                    if (element.matches(selector)) {
                        selectedItems.push([selector.split('.')[0], element.innerText]);
                    }
                }
            }

            return selectedItems;
        }''', contentSelector)

        previousHeight = await page.evaluate("document.body.scrollHeight")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.waitForFunction(f'document.body.scrollHeight > {previousHeight}')
        await asyncio.sleep(1)

        items = selectedItems

    return items

async def delPopUp(page,popup):
    try:
        # Replace the CSS selector with the appropriate selector for the pop-up element
        await page.waitForSelector(popup[0], {'timeout': 5000})
        await page.click(popup[0])
        await page.waitForSelector(popup[0], {'hidden': True, 'timeout': 5000})
    except pyppeteer.errors.TimeoutError:
        pass  # Pop-up not found or already closed


# calling the scraper
async def scraper(elements, pageUrl):
    executablePath='C:\Program Files\Google\Chrome\Application\chrome.exe'
    browser = await pyppeteer.launch(
        headless=False,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        executablePath=executablePath
    )
    page = await browser.newPage()
    await page.goto(pageUrl)

    if(elements[0]==''):
        elements.pop(0)
    else:
        await delPopUp(page,elements)
        elements.pop(0)
    
    print(elements)
    items = await scrapeInfiniteScrollItems(page, elements, 5)
    uniqueItems = []
    seenItems = set()
    for item in items:
        itemTuple = tuple(item)
        if itemTuple not in seenItems:
            uniqueItems.append(item)
            seenItems.add(itemTuple)
    
    await browser.close()
    return uniqueItems




# generic webscraper
def genericScraper(listOfElements: list, pageurl):
    sys.stdout.reconfigure(encoding='utf-8') #so that other languages can be printed
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
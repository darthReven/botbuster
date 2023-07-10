# social media scraper moduels
import asyncio
import pyppeteer
from pyppeteer import launch
import os
# generic webscraper modules
import requests
import sys
from bs4 import BeautifulSoup
from fastapi import HTTPException
from urllib.parse import urljoin

# social media scraper
async def scrape_infinite_scroll_items(page, content_selector, item_target_count):
    await asyncio.sleep(2.5)
    items = []

    while item_target_count > len(items):
        selected_items = await page.evaluate('''(contentselector) => {
            const selected_items = [];
            const elements = Array.from(document.querySelectorAll("*"));

            for (const element of elements) {
                for (const selector of contentselector) {
                    if (element.matches(selector)) {
                        selected_items.push([selector.split('.')[0], element.innerText]);
                    }
                }
            }

            return selected_items;
        }''', content_selector)

        previous_height = await page.evaluate("document.body.scrollHeight")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.waitForFunction(f'document.body.scrollHeight > {previous_height}')
        await asyncio.sleep(1)

        items = selected_items

    return items

async def del_pop_up(page, popup):
    try:
        # Replace the CSS selector with the appropriate selector for the pop-up element
        await page.waitForSelector(popup[0], {'timeout': 5000})
        await page.click(popup[0])
        await page.waitForSelector(popup[0], {'hidden': True, 'timeout': 5000})
    except pyppeteer.errors.TimeoutError:
        pass  # Pop-up not found or already closed

# find chrome path
def get_chrome_path():
    print("test")
    directories = ["C:\\Program Files", "C:\\Program Files (x86)"]
    # Search for Chrome in Program Files directories
    for file in directories:
        chrome_path = os.path.join(file, "Google", "Chrome", "Application", 'chrome.exe')
        if os.path.isfile(chrome_path):
            print(chrome_path)
            return chrome_path
    return None

# calling the scraper
async def scraper(elements, page_url):
    print("getting chrome path")
    chrome_path = get_chrome_path()
    cookies = os.path.join(os.getcwd(), 'scraper_cookies')
    print(cookies)
    browser = await launch(
        headless=False,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        executablePath=chrome_path,
        userDataDir=cookies
    )
    page = await browser.newPage()
    await page.goto(page_url)

    if(elements[0]==''):
        elements.pop(0)
    else:
        await del_pop_up(page, elements)
        elements.pop(0)
    
    print(elements)
    items = await scrape_infinite_scroll_items(page, elements, 5)
    unique_items = []
    seen_items = set()
    for item in items:
        item_tuple = tuple(item)
        if item_tuple not in seen_items:
            unique_items.append(item)
            seen_items.add(item_tuple)
    
    await browser.close()
    return unique_items

# generic webscraper
def genericScraper(list_of_elements: list, page_url, url, splitter):
    sys.stdout.reconfigure(encoding='utf-8')  # so that other languages can be printed
    extracted_text = []
    connected_pages = [page_url]
    base_url = page_url.rstrip(splitter)
    page_param = page_url.rsplit(splitter, 1)[-1] #find which page this is
    if "page" not in page_param: #if current page is the first page
          # Check for connected pages starting from page 2
            page_num = 2
            while True:
                page_param = url.replace("*",str(page_num))
                page_url = f"{base_url}{splitter}{page_param}"
                response = requests.get(page_url)
                if response.status_code == 200:
                    # Check if the URL has changed due to redirection
                    new_url = response.url
                    if new_url != page_url:
                        break  # Break the loop if the URL remains the same after redirection
                    connected_pages.append(page_url)
                    page_num = int(page_num)
                    page_num += 1
                  
                else:
                    break
    else:
        base_url = page_url.rstrip(splitter)
        first_page = base_url.rsplit(splitter, 1)[0] #get first page
        connected_pages.append(first_page)
        page_num_param = page_url.split(splitter)[-1]
        page_num = "".join(filter(str.isdigit, page_num_param))
        num_of_loops = 0
        while True: #check for pages after current page
                num_of_loops += 1 #to get the original page number later on
                last_slash_index = base_url.rfind(splitter)
                page_url = base_url[:last_slash_index]
                page_param = url.replace("*",str(page_num))
                page_url = f"{page_url}{splitter}{page_param}" #replace page number in url with the new one
                response = requests.get(page_url)
                if response.status_code == 200:
                    # check if the URL has changed due to redirection
                    new_url = response.url
                    if new_url != page_url:
                        page_num -= num_of_loops+1 #one page before original page number
                        while True:
                            last_slash_index = base_url.rfind('/')
                            page_url = base_url[:last_slash_index]
                            page_param = url.replace("*",str(page_num))
                            page_url = f"{page_url}{splitter}{page_param}" #replace page number in url with the new one
                            response = requests.get(page_url)
                            if response.status_code == 200:                              
                                # check if the URL has changed due to redirection
                                new_url = response.url
                                if new_url != page_url:
                                    break  # break the loop if the URL remains the same after redirection
                                connected_pages.append(page_url)
                                page_num = int(page_num)
                                page_num -= 1                     
                            else:
                                break
                        break
                    connected_pages.append(page_url)
                    page_num = int(page_num)
                    page_num += 1
                else:
                    break
    
    connected_pages.sort(key=lambda x: (x,'page' not in x)) #sort according to page number
    print(connected_pages)

#scraping starts here
    for page_url in connected_pages:
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for element in list_of_elements:
                if "." in element:
                    split_element = element.split(".", 1)
                    element_type = split_element[0]
                    element_class = split_element[1]
                    elements = soup.find_all(element_type, class_=element_class)
                    for index, element in enumerate(elements):
                        text = element.get_text(strip=True)
                        extracted_text.append([element_type, text, index])
                else:
                    element_type = element
                    elements = soup.find_all(element_type)
                    for index, element in enumerate(elements):
                        text = element.get_text(strip=True)
                        extracted_text.append([element_type, text, index])
            extracted_text.sort(key=lambda x: x[2] if len(x) > 2 else 0)  # sort elements based on their order in the HTML
            extracted_text = [[element_type, text] for element_type, text, *_ in extracted_text] 
        else:
            raise HTTPException(status_code=400, detail="Target website could not be scraped due to errors on that website, please check the URL again.")
   
    return extracted_text




    





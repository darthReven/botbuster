# social media scraper modules
import asyncio
import pyppeteer
from pyppeteer import launch
import os
import platform
import random
# generic webscraper modules
import requests
import sys
from bs4 import BeautifulSoup
from fastapi import HTTPException
from urllib.parse import urljoin

# social media scraper
async def scrape_infinite_scroll_items(page, content_selector, item_target_count, max_retries=10):
    await asyncio.sleep(2.5)
    items = []
    previous_height = 0
    retries = 0

    while retries < max_retries:
        selected_items = await page.evaluate('''(content_selector, previous_height) => {
            const selected_items = [];
            const elements = Array.from(document.querySelectorAll("*"));

            for (const element of elements) {
                for (const selector of content_selector) {
                    if (element.matches(selector)) {
                        selected_items.push([selector.split('.')[0], element.innerText]);
                    }
                }
            }

            return selected_items;
        }''', content_selector, previous_height)

        items.extend(selected_items)
        current_height = await page.evaluate("document.body.scrollHeight")

        if current_height == previous_height:
            # Reached the bottom of the page, no more items to load
            break

        previous_height = current_height

        if len(items) >= item_target_count:
            break

        # Check if it's still possible to scroll down
        can_scroll_down = await page.evaluate("window.innerHeight + window.scrollY < document.body.scrollHeight")

        if can_scroll_down:
            # Scroll down to trigger more content loading
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            # Introduce some randomness to the sleep interval to avoid triggering anti-scraping measures
            sleep_interval = random.uniform(2, 3)
            await asyncio.sleep(sleep_interval)

            retries += 1
        else:
            # If it's not possible to scroll down, break the loop
            break

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
    system = platform.system()
    if system == "Windows":
        directories = ["C:\\Program Files", "C:\\Program Files (x86)"]
        # Search for Chrome in Program Files directories
        for file in directories:
            chrome_path = os.path.join(file, "Google", "Chrome", "Application", 'chrome.exe')
            if os.path.isfile(chrome_path):
                return chrome_path
    elif system == "Linux":
        directories = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
        ]
        for chrome_path in directories:
            if os.path.isfile(chrome_path):
                return chrome_path
    return False

# calling the scraper
async def scraper(elements,settings, page_url):
    chrome_path = get_chrome_path()
    cookies = os.path.join(os.getcwd(), 'scraper_cookies')
    if(chrome_path==False):
        browser = await launch(
        headless=True,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        userDataDir=cookies
        )
    else:
        browser = await launch(
            headless=True,
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False,
            executablePath=chrome_path,
            userDataDir=cookies
        )
    page = await browser.newPage()
    await page.goto(page_url)

    # check if website has any popups defined
    if(settings[0]==''):
        pass
    else:
        await del_pop_up(page, settings)
    num_of_items=settings[1]
    items = await scrape_infinite_scroll_items(page, elements, num_of_items)
    # filtering to avoid duplicate content
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
def generic_scraper(list_of_elements: list, page_url, url, splitter):
    sys.stdout.reconfigure(encoding='utf-8')  # so that other languages can be printed
    extracted_text = []
    connected_pages = [page_url]
    base_url = page_url.rstrip(splitter)
    page_param = page_url.rsplit(splitter, 1)[-1] #find which page this is
    url_placeholder = url.strip('*')
    if url_placeholder not in page_param or (url_placeholder == "" and page_param == ""): #if current page is the first page
          # Check for connected pages starting from page 2
            page_num = 2
            while True:
                before_page_url = page_url
                page_param = url.replace("*",str(page_num))
                page_url = f"{base_url}{splitter}{page_param}"
                if before_page_url==page_url: #check if there is a page param to see if this website is single paged
                    break
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
        page_num_param = page_url.split(splitter)[-1]
        page_num = "".join(filter(str.isdigit, page_num_param))
        if page_num != "":
            first_page = base_url.rsplit(splitter, 1)[0] #get first page
            connected_pages.append(first_page)
            num_of_loops = 0
            page_num = int(page_num)
            original_page_num = page_num
            page_num+=1
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
                                    page_num -= 1                     
                                else:
                                    break
                            break
                        connected_pages.append(page_url)
                        page_num += 1
                    else:
                        while original_page_num > 2:   #for pages that doesnt redirect, we need to check if there are pages before the page that the user had input
                                page_num = original_page_num - 1
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
                                else:
                                    break
                                original_page_num -=1
                                
                        break
        else:
            connected_pages=connected_pages
    
    connected_pages.sort(key=lambda x: (len(x), url_placeholder not in x, x)) #sort according to page number
    

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




    





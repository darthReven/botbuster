import requests
from bs4 import BeautifulSoup
import sys

request_url = "https://forums.hardwarezone.com.sg/threads/malaysia-graduate-are-fortunate-than-china-graduate-i-see-china-youth-unemployment-hit-20-8.6914444/"

sys.stdout.reconfigure(encoding='utf-8')

response = requests.get(request_url)
if response.status_code == 200: 
    soup = BeautifulSoup(response.content, 'html.parser')

    extracted_text = []

    hardwarezone_h1_element = soup.find('h1', class_='p-title-value')
    if hardwarezone_h1_element:
        hardwarezone_h1_text = hardwarezone_h1_element.get_text(strip=True)
        extracted_text.append(['h1', hardwarezone_h1_text])

    reddit_h1_element = soup.find('h1')
    if reddit_h1_element:
        reddit_h1_text = reddit_h1_element.get_text(strip=True)
        extracted_text.append(['h1', reddit_h1_text]) 

    # h1_elements = soup.find_all('h1', class_="_eYtD2XCVieq6emjKBH3m")
    # for h1_element in h1_elements:
    #     h1_text = h1_element.get_text(strip=True)
    #     extracted_text.append(['h1', h1_text])

    p_elements = soup.find_all('p')
    for p_element in p_elements:
        p_text = p_element.get_text(strip=True)
        extracted_text.append(['p', p_text])

    pre_elements = soup.find_all('pre')
    for pre_element in pre_elements:
        pre_text = pre_element.get_text(strip=True)
        extracted_text.append(['pre', pre_text])
    
    chan_elements = soup.find_all('blockquote', class_="postMessage")
    for pre_element in chan_elements:
        pre_text = pre_element.get_text(strip=True)
        extracted_text.append(['pre', pre_text])

    div_wrapper = soup.select("div.bbWrapper:not(.messageAdBanner, .bbCodeBlock--quote, .bbCodeBlock, .bbCodeBlock--expandable, .js-expandWatch, .is-expandable, .bbCodeBlock-title, .bbCodeBlock-content, a, blockquote, .pairs, .pairs--justified, dl)")
    for element in div_wrapper:
        extracted_text.append([element.name, element.get_text(strip=True)])

    print(extracted_text)
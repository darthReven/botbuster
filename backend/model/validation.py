import html
import re

def sanitise(data):
    if isinstance(data, dict):
        return {sanitise(key): sanitise(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitise(item) for item in data]
    elif isinstance(data, str):
        return html.escape(data)  # Escape the string
    else:
        return data


def decode(data):
    if isinstance(data, dict):
        return {decode(key): decode(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [decode(item) for item in data]
    elif isinstance(data, str):
        return html.unescape(data)
    else:
        return data
    

def is_valid_url(url_string):
    url_pattern = r"^(https?):\/\/[^\s/$.?#].[^\s]*$"
    return bool(re.match(url_pattern, url_string))


# tbh yall wan update the add api thing right? so i made smth but nvr test yet
# in main.py:
# if(validation.check_add_api(req)==False):
        # raise HTTPException (status_code = 400, detail = "Invalid Input!")
def check_add_api(api):
    def recursion(data):
        if isinstance(api, dict):
            return {recursion(key): recursion(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [recursion(item) for item in data]
        elif isinstance(data, str):
            return data
        elif isinstance(data,bool):
            return data
        else:
            return False
    try:
        if(is_valid_url(api["api_details"]["target"])==False or recursion(api)==False):
            return False
        else:
            return True

    except KeyError:
        return False
    
def check_text(text):
    if not isinstance(text, str):
        return False
    return bool(text.strip())

# web scraper setings validation funcs
def check_elements(elements):
    # loop through elements, check if they match the regex
    compound_selector_pattern = r"^(?:[a-zA-Z_][\w-]*\.)+[a-zA-Z_][\w-]*$|^([a-zA-Z_][\w-]*)$"
    return bool(re.match(compound_selector_pattern, elements))
    pass


def check_domain(domain):
    # check if the regex matches the domain
    domain_name_pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$"
    return bool(re.match(domain_name_pattern, domain))
    pass
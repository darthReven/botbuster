'''
AY2023/24 Final Year Project 
DISM3A68

p2104092 Lucas Quek
p2104104 Elliot Ang
p2128511 Kara Huang
p2128649 Cheong Yue Ming
P2128962 Sibi Srinivas S/O Ganesan
'''

import html
import re

from jsonschema import ValidationError,validate

def validate_api_details(api_config):
    return True

def check_add_api(api_config):
    common_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "patternProperties": {
            ".*": {
                "type": "object",
                "properties": {
                    "target": {"type": "string"},
                    "body_key": {"type": "string"},
                    "data_type": {"type": "string"},
                    "headers": {"type": "object"},
                    "body": {"type": "object"}
                },
                "required": ["target", "body_key", "data_type", "headers", "body"]
            }
        }
    }

    try:
        validate(api_config, common_schema)
        return True
    except ValidationError as e:
        return False

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
    
def check_text(text):
    if not isinstance(text, str):
        return False
    return bool(text.strip())

# web scraper setings validation funcs
def check_elements(elements):
    element_regex = r"^(?:[a-zA-Z_][\w-]*\.)+[a-zA-Z_][\w-]*$|^([a-zA-Z_][\w-]*)$"
    elements = elements.replace(" ", "")

    if bool(re.match(element_regex, elements)):
        html_elements = [
            "a", "abbr", "acronym", "address", "area", "article", "aside", "audio", "b", "base", "bdi", "bdo", "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code", "col", "colgroup", "data", "datalist", "dd", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt", "em", "embed", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hgroup", "hr", "html", "i", "iframe", "img", "input", "ins", "kbd", "label", "legend", "li", "link", "main", "map", "mark", "menu", "meta", "meter", "nav", "noscript", "object", "ol", "optgroup", "option", "output", "p", "param", "picture", "pre", "progress", "q", "rb", "rp", "rt", "ruby", "s", "samp", "script", "section", "select", "small", "source", "span", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track", "u", "ul", "var", "video", "wbr", "xmp"
        ]
        element = elements.split('.')
        for count in html_elements:
            if count == element[0].lower():
                return True
        return False
    else:
        return False

def check_domain(domain):
    # check if the regex matches the domain
    domain = domain.replace(" ","")
    if(domain=='default'):
        return True
    domain_name_pattern = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" +"+[A-Za-z]{2,6}"
    return bool(re.match(domain_name_pattern, domain))
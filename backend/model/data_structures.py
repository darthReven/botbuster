'''
AY2023/24 Final Year Project 
DISM3A68

p2104092 Lucas Quek
p2104104 Elliot Ang
p2128511 Kara Huang
p2128649 Cheong Yue Ming
P2128962 Sibi Srinivas S/O Ganesan
'''

from pydantic import BaseModel

class split_text (BaseModel):
    list_of_apis: list
    text: str

class check_text (BaseModel):
    list_of_apis: list
    text: str

class add_api (BaseModel):
    name: str
    category: str
    target: str
    body_key: str
    data_type: str
    headers: dict
    body: dict
    path_to_general_score: str
    path_to_sentence_score: list
    description: str
    score_type: str

class web_scraper (BaseModel):
    page_url: str

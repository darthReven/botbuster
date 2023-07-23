from pydantic import BaseModel

class split_text (BaseModel):
    list_of_apis: list
    text: str

class check_text (BaseModel):
    list_of_apis: list
    text: str

class add_api (BaseModel):
    api_details: dict
    api_name: str

class web_scraper (BaseModel):
    page_url: str

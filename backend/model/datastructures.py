from pydantic import BaseModel

class checkText (BaseModel):
    list_of_apis: list
    text: str

class addApi (BaseModel):
    api_details: dict
    api_name: str
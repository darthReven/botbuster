from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import uvicorn
import misinfo as ms

misinfo= FastAPI()

misinfo.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Text(BaseModel):
    text: str

@misinfo.on_event("startup")
async def startup_event():
    ms.trainModel()
    # print('model has been trained, now responding to requests.')

@misinfo.post("/predict/")
def predict(text: Text):
    # print(text)
    try:
        predText = text.dict()["text"]
        prediction=ms.predictText(predText)
        # print(prediction)
        return({"prediction":f"{prediction}"})
    except:
        raise HTTPException(status_code = 500, detail = "Internal Server Error")

if __name__ == "__main__":
    uvicorn.run(misinfo, port=8001)
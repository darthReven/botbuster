# uvicorn main:misinfo --reload
from fastapi import FastAPI
from pydantic import BaseModel

import misinfo as ms

misinfo=FastAPI()
class Text(BaseModel):
    text: str

@misinfo.on_event("startup")
async def startup_event():
    ms.trainModel()
    print('model has been trained, now responding to requests.')

@misinfo.post("/predict/")
def predict(text: Text):
    # print(text)
    predText = text.dict()["text"]
    prediction=ms.predictText(predText)
    return({"prediction": prediction})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(misinfo, host="0.0.0.0", port=8001)

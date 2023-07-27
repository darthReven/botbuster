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
    # print('model has been trained, now responding to requests.')
    text = """Those who love travelling Japan by rail, brace yourselves for more bad news: The Japan Railways (JR) Group’s regional train passes will cost up to 50 per cent more from Oct 1.

This announcement comes after the transport authority said in April that the price of its nationwide passes will rise by more than 60 per cent in October.

Prices for JR East and JR Central, which cover the popular Tokyo, Nagano and Tohoku areas, saw the largest price increases.

For instance, the JR East Tohoku Area Pass, which covers the Kanto and Tohoku regions, will rise from 20,000 yen (S$189) to 30,000 yen, a 50 per cent increase. The five-day pass offers unlimited travel on JR trains, including the high-speed shinkansen bullet trains, and JR buses.

The three-day JR Tokyo Wide Pass is also set to rise by 47 per cent from 10,180 yen to 15,000 yen.

The five-day Takayama-Hokuriku Area Tourist Pass, which offers train rides connecting Nagoya with Takayama and Osaka with Kanazawa, will be priced at 19,800 yen, up 39 per cent from the current 14,260 yen.

JR Group said on Wednesday that prices will be revised as it will expand the lines covered by the passes and introduce automatic ticket gates. It will also increase the number of seats allocated for reservations for some passes.

The transport authority added that pass holders will receive certain perks, such as discounts at selected stores.

Meanwhile, the price hikes for JR West, JR Kyushu and JR Hokkaido were less drastic, with the five-day Hokkaido Rail Pass to rise by 5 per cent from 19,000 yen to 20,000 yen.

The five-day Kansai Wide Area Pass, which takes tourists to popular areas like Himeji and Nara, will be priced at 12,000 yen, up 20 per cent from the current 10,000 yen.

In April, the JR Group left many travellers shocked and disappointed when it announced the price hikes for the nationwide passes.

A single adult pass that will cover all JR lines for seven days will cost 50,000 yen come Oct 1, up 68.6 per cent from the current 29,650 yen.

The 14-day pass will cost 80,000 yen, up from 47,250 yen now.

Rides on the fastest Nozomi and Mizuho trains will also be available with the new nationwide pass at an additional cost, depending on the distance travelled. For example, it will be 4,180 yen for a trip from Tokyo to Kyoto.

Prices for children aged between six and 11 are half that of the adult passes.

The old passes will remain on sale until Sept 30.
"""
    
    prediction=ms.predictText(text)
    print(prediction)


@misinfo.post("/predict/")
def predict(text: Text):
    # print(text)
    text = text.dict()["text"]
    prediction=ms.predictText(text)
    return({"prediction": prediction})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(misinfo, host="0.0.0.0", port=8001)

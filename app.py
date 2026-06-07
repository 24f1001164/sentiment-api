from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

POSITIVE = {
    "love","great","excellent","amazing","awesome",
    "happy","good","fantastic","wonderful","best",
    "like","enjoy","brilliant","perfect"
}

NEGATIVE = {
    "hate","bad","terrible","awful","worst",
    "sad","angry","upset","horrible",
    "poor","disappointed","annoying"
}

def predict_sentiment(text: str):
    text = text.lower()

    pos = sum(word in text for word in POSITIVE)
    neg = sum(word in text for word in NEGATIVE)

    if pos > neg:
        return "happy"
    elif neg > pos:
        return "sad"
    else:
        return "neutral"

@app.post("/sentiment")
async def sentiment(req: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": predict_sentiment(sentence)
            }
            for sentence in req.sentences
        ]
    }

@app.get("/")
async def root():
    return {"status": "running"}

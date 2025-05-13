from fastapi import APIRouter
from pydantic import BaseModel
from textblob import TextBlob


router = APIRouter(prefix="/api", tags=["Analyzer"])


class TextIn(BaseModel):
    text: str


class SentimentOut(BaseModel):
    sentiment: str
    polarity: float
    subjectivity: float


@router.post("/analyze", response_model=SentimentOut)
async def analyze_sentiment(payload: TextIn):
    blob = TextBlob(payload.text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    sentiment = "neutral"
    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"

    return SentimentOut(
        sentiment=sentiment, polarity=polarity, subjectivity=subjectivity
    )

from pydantic import BaseModel, Field


class TextIn(BaseModel):
    text: str = Field(..., max_length=500, description="Max length: 500")


class SentimentOut(BaseModel):
    sentiment: str
    polarity: float
    subjectivity: float

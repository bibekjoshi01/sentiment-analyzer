from pydantic import BaseModel, Field
from typing import Dict


class TextIn(BaseModel):
    text: str = Field(..., max_length=500, description="Max length: 500")


class SentimentOut(BaseModel):
    sentiment: str
    polarity: float
    subjectivity: float


class EmotionResponse(BaseModel):
    dominant_emotion: str
    emotions: Dict[str, float]
    confidence: float
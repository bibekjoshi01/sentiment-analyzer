from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from textblob import TextBlob
from PIL import Image
from io import BytesIO
from deepface import DeepFace
import numpy as np

from app.database import get_db
from app.dependencies import get_current_user, oauth2_scheme
from app.models.analyzer import AnalysisRequest
from app.models.user import User
from app.schemas.analyzer import EmotionResponse, SentimentOut, TextIn


router = APIRouter(prefix="/api/analyze", tags=["Analyzer"])


def validate_request_count(db: Session, user: User):
    today = datetime.now().date()
    day_start = datetime(today.year, today.month, today.day)
    day_end = day_start + timedelta(days=1)

    request_count = (
        db.query(AnalysisRequest)
        .filter(
            AnalysisRequest.user_id == user.id,
            AnalysisRequest.timestamp >= day_start,
            AnalysisRequest.timestamp < day_end,
        )
        .count()
    )

    return request_count


@router.post("/text", response_model=SentimentOut)
async def analyze_text_sentiment(
    payload: TextIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
):

    if validate_request_count(db, user) >= 10:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Daily request limit reached (10 per day).",
        )

    blob = TextBlob(payload.text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    sentiment = "neutral"
    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"

    db.add(AnalysisRequest(user_id=user.id, text=payload.text))
    db.commit()

    return SentimentOut(
        sentiment=sentiment, polarity=polarity, subjectivity=subjectivity
    )


@router.post("/image", response_model=EmotionResponse)
async def analyze_image_sentiment(
    file: UploadFile,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
):

    if validate_request_count(db, user) >= 10:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Daily request limit reached (10 per day).",
        )

    image = Image.open(BytesIO(await file.read()))

    try:
        np_image = np.array(image)
        result = DeepFace.analyze(np_image, actions=["emotion"])
        emotion_data = result[0]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Emotion analysis failed: {str(e)}"
        )

    db.add(AnalysisRequest(user_id=user.id))
    db.commit()
    return {
        "dominant_emotion": emotion_data["dominant_emotion"],
        "emotions": emotion_data["emotion"],
        "confidence": emotion_data["emotion"][emotion_data["dominant_emotion"]],
    }

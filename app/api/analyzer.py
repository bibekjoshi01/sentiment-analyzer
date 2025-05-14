from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from textblob import TextBlob
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, oauth2_scheme
from app.models.analyzer import AnalysisRequest
from app.models.user import User
from app.schemas.analyzer import SentimentOut, TextIn


router = APIRouter(prefix="/api/analyze", tags=["Analyzer"])


@router.post("/text", response_model=SentimentOut)
async def analyze_sentiment(
    payload: TextIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
):
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

    if request_count >= 10:
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

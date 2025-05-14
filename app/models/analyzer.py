from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class AnalysisRequest(Base):
    __tablename__ = "analysis_request"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    timestamp = Column(DateTime, default=datetime.now)

    user = relationship("User")

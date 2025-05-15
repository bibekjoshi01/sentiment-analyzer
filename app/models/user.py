from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

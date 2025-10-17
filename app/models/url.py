
from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime
from app.database import Base

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(String, primary_key=True)
    original = Column(String, nullable=False)
    short = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    clicks = Column(Integer, default=0)

from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    steps = Column(Text)
    root_cause = Column(String(255))
    resolution = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

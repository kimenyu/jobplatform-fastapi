from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from datetime import datetime
from app.database.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("users.id"))
    file_path = Column(String, nullable=False)
    parsed_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    applicant = relationship("User", backref="resumes")

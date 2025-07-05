from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from datetime import datetime
from app.database.base import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    applicant_id = Column(Integer, ForeignKey("users.id"))

    resume_file_path = Column(String, nullable=True)
    cover_letter = Column(Text, nullable=True)
    parsed_resume = Column(JSON, nullable=True)
    status = Column(String, default="pending")  # 'pending', 'reviewed', 'rejected'

    job = relationship("Job", back_populates="applications")
    applicant = relationship("User", back_populates="applications")

    created_at = Column(DateTime, default=datetime.utcnow)

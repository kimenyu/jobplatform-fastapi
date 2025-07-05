from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from datetime import datetime
from app.database.base import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    skills_required = Column(JSON, nullable=True)

    posted_by = Column(Integer, ForeignKey("users.id"))
    employer = relationship("User", back_populates="jobs")

    applications = relationship("Application", back_populates="job", cascade="all, delete")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.application import Application

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'admin', 'employer', 'applicant'
    is_active = Column(Boolean, default=True)

    # Relationships
    jobs = relationship("Job", back_populates="employer", cascade="all, delete")
    applications = relationship(Application, back_populates="applicant", cascade="all, delete")


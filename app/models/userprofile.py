from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    full_name = Column(String)
    bio = Column(Text, nullable=True)
    linkedin = Column(String, nullable=True)
    github = Column(String, nullable=True)
    website = Column(String, nullable=True)

    user = relationship("User", backref="profile")

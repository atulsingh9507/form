# models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    fullName = Column(String, index=True)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    resumePath = Column(String)  # Store full path to resume file
    photoPath = Column(String, nullable=True)  # Store full path to photo file if uploaded
    address = Column(String)
    position = Column(String)
    gender = Column(String)
    qualification = Column(String)
    reference = Column(String, nullable=True)

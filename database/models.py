from sqlalchemy import Column, Integer, String, Float, Text, DateTime
import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import Base, engine

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), index=True)
    skills = Column(Text)
    predicted_role = Column(String(255))
    ats_score = Column(Float)
    jd_match = Column(Float)
    missing_skills = Column(Text)
    resume_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class TrainingData(Base):
    __tablename__ = "training_data"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    role = Column(String(255), nullable=False)

# Ensure tables are created
Base.metadata.create_all(bind=engine)

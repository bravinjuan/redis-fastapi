# IMPORTS -------------------------------------------------------------
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Float, Boolean, null
from sqlalchemy.orm import relationship
from db_config import Base
# IMPORTS -------------------------------------------------------------


class Consultant(Base):
    __tablename__ = "Consultant"
    id = Column(String(255), primary_key=True, index=True)
    Name = Column(String(255), nullable=False)
    LastName = Column(String(255))
    Legajo = Column(String(50))
    StartDate = Column(DateTime)
    EndDate = Column(DateTime)
    Seniority = Column(String(50))
    Billable = Column(Boolean)
    Availability = Column(Float)
    EnglishLevel = Column(Integer)
    DeletedDate = Column(DateTime)

from sqlalchemy import Column, Integer, String
from database import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    domain = Column(String)
    duration = Column(Integer)
    category = Column(String)

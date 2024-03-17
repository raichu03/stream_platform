from sqlalchemy import Column, Integer, String
from database import Base


class Stream(Base):
    __tablename__ = "streams"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    location = Column(String)
    date = Column(String)
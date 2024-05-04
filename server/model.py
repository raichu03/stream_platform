from sqlalchemy import Column, Integer, String
from database import Base


class Stream(Base):
    __tablename__ = "streams"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    lat = Column(Integer)
    long = Column(Integer)
    date = Column(String)

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    classe = Column(String)
    lat = Column(Integer)
    long = Column(Integer)
    date = Column(String)
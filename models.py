from sqlalchemy import Boolean, Column, Integer, String

from db import Base

class Camp(Base):
    __tablename__ = "camps"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
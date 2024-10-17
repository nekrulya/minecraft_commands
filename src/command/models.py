from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Command(Base):
    __tablename__ = 'command'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_by = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
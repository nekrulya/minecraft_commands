from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from src.database import Base
from datetime import datetime


class Command(Base):
    __tablename__ = 'command'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    created_by = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
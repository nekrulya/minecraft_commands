from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from src.database import Base


class Command(Base):
    __tablename__ = 'command'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_by = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

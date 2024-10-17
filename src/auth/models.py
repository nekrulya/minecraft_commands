from sqlalchemy import Table, Column, Integer, String
from src.database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)

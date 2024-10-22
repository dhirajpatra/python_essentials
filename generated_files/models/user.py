from sqlalchemy import Column, Integer, String
from database import metadata, database

class User:
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), index=True)
    email = Column(String(length=100), unique=True, index=True)
    password = Column(String(length=100))

# Create the table (this should be done using migrations in production)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///./test.db')
metadata.create_all(engine)

from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "sqlite:///./test.db"

database = Database(DATABASE_URL)
metadata = MetaData()

# Create an engine
engine = create_engine(DATABASE_URL)

# Create all tables
metadata.create_all(engine)

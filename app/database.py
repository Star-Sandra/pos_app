import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# 1. Search for and load the .env file from the root folder
load_dotenv(find_dotenv())

# 2. Extract the secret database string safely
DATABASE_URL = os.getenv("DATABASE_URL")

# 3. Safety check: Stop the app immediately if the secret is missing
if not DATABASE_URL:
    raise ValueError(
        "CRITICAL ERROR: DATABASE_URL is missing! "
        "Make sure you created a '.env' file at the root level."
    )
    
engine = create_engine(DATABASE_URL, echo=False, future=True)
session = sessionmaker(autocommit=False, autoflash=False, bind= engine)
base = declarative_base()
def get_db():
    db=session()
    try: 
        yield db
    finally: 
        db.close()

def create_tables():
    import app.models as models


 

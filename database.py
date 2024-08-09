import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy import create_engine


load_dotenv()  

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
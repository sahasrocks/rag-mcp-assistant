import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    echo=False
)

SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False)
)
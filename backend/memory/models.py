from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from memory.database import engine

Base = declarative_base()


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), index=True, nullable=False)
    role = Column(String(20), nullable=False)  # user / assistant
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)
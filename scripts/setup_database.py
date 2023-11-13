from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

DATABASE_URL = "sqlite:///./conversation.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def setup_database():
    Base.metadata.create_all(bind=engine)

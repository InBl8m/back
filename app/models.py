from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Conversation(Base):
    __tablename__ = "ai_conversation"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, index=True)
    order = Column(Integer, index=True)
    message_text = Column(String, index=True)
    processed_status = Column(Boolean, default=False)
    audio_link = Column(String, default=None)
    last_in_list = Column(Boolean, default=False)


class Audio(Base):
    __tablename__ = "uploaded_audio"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    question_text = Column(String, default=None)

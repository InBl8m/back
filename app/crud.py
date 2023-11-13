from sqlalchemy.orm import Session
from app.models import Conversation, Audio


def get_answer_by_id(db: Session, question_id: int, order: int):
    db_answer = db.query(Conversation).filter(Conversation.question_id == question_id,
                                              Conversation.order == order).first()

    return db_answer


def get_audio_by_id(db: Session, audio_id: int):
    return db.query(Audio).filter(Audio.id == audio_id).first()


def create_conversation(db: Session, message_text: str, conv_id: int, order: int):
    db_conversation = Conversation(message_text=message_text, question_id=conv_id, order=order)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def create_audio_by_text(db: Session, question_text: str):
    db_audio = Audio(question_text=question_text)
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio


def create_audio(db: Session, filename: str):
    db_audio = Audio(filename=filename)
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio

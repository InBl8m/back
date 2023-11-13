import os
from celery import Celery
from celery.result import AsyncResult
from app.database import SessionLocal
from app.crud import create_conversation
from app.models import Conversation, Audio
from answer.tts import text_to_speech
from answer.stt import get_question
from answer.by_chanks import chat_generate


app = Celery("app", broker="redis://localhost:6379/0")


@app.task
def process_text_task(conversation_id):
    db = SessionLocal()
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation:
        audio_link = 'http://127.0.0.1:8000/uploads/answers/' + text_to_speech(conversation.message_text)
        conversation.processed_status = True
        conversation.audio_link = audio_link
        db.commit()
    db.close()


@app.task
def process_audio(audio_id):
    db = SessionLocal()
    #  открываем вопрос в БД по id
    question = db.query(Audio).filter(Audio.id == audio_id).first()
    #  определяем полный путь к аудиофайлу
    full_path = os.getcwd() + '/uploads/' + question.filename
    # отправляем аудиофайл на распознавание речи
    question_text = get_question(full_path)
    #  определяем id вопроса
    question_id = question.id
    #  записываем распознанный текст в БД
    question.question_text = question_text
    db.commit()
    if question_text != 'Голос не распознан':
        mark_last(chat_generate(question_text, question_id))
    else:
        conversation = create_conversation(db, 'Голос не распознан', question_id, 1)
        conversation.processed_status = True
        conversation.last_in_list = True
        db.commit()
    db.close()


@app.task
def process_text(audio_id):
    db = SessionLocal()
    question = db.query(Audio).filter(Audio.id == audio_id).first()
    question.filename = '/answers/' + text_to_speech(question.question_text)
    mark_last(chat_generate(question.question_text, question.id))
    db.commit()
    db.close()


def mark_last(last_id: int):
    db = SessionLocal()
    conversation = db.query(Conversation).filter(Conversation.id == last_id).first()
    if conversation:
        conversation.last_in_list = True
        db.commit()
    db.close()

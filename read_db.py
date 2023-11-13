from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Conversation, Audio

# Создайте подключение к базе данных
DATABASE_URL = "sqlite:///./conversation.db"
engine = create_engine(DATABASE_URL)

# Создайте сессию
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

questions = session.query(Conversation).all()

# Выведите считанные вопросы
for question in questions:
    print(f"ID: {question.id}")
    print(f"ID вопроса: {question.question_id}")
    print(f"ID порядок: {question.order}")
    print(f"Текст сообщения: {question.message_text}")
    print(f"Статус обработки: {question.processed_status}")
    print(f"Ссылка на аудио: {question.audio_link}")
    print(f"Последний чанк: {question.last_in_list}")
    print()

questions = session.query(Audio).all()
for question in questions:
    print(f"ID: {question.id}")
    print(f"Название файла: {question.filename}")
    print(f"Текст аудио: {question.question_text}")
    print()

session.close()

import time
from answer.play_sound import play_audio
from answer.by_chanks import chat_generate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Conversation

DATABASE_URL = "sqlite:///./conversation.db"


def get_from_db(desired_ids):
    while True:
        print('here')
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = Session()
        conversation = session.query(Conversation).filter(Conversation.id == desired_ids[0]).first()
        session.close()
        print('There')
        if conversation:
            if conversation.complete_status:
                break  # Выход из цикла, так как complete_status стал True
        time.sleep(1)
    conversations = session.query(Conversation).filter(Conversation.id.in_(desired_ids)).all()
    for conversation in conversations:
        session = Session()
        play_audio(conversation.audio_link)
        session.close()
        # Теперь у вас есть список строк (объектов Conversation) с определенными идентификаторами


if __name__ == '__main__':
    waw_list = chat_generate("Привет, как дела?")
    # waw_list = chat_generate("Расскажи про машинное обучение")
    print(waw_list)
    get_from_db(waw_list)
    # audio_file_path = f"{1697659221}.wav"  # Replace with the actual path to your audio file
    # play_audio(audio_file_path)
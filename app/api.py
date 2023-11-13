import os
import uuid
from fastapi import APIRouter, UploadFile, HTTPException
from schemas.schemas import ConversationResponse, TextRequest, AudioResponse, TextMessageRequest
from app.crud import create_conversation, create_audio, get_audio_by_id, get_answer_by_id, create_audio_by_text
from app.database import SessionLocal
from app.tasks import process_text_task, process_audio, process_text


router = APIRouter()


@router.post("/process_text/", response_model=ConversationResponse)
def create_conversation_endpoint(text_request: TextRequest):
    db = SessionLocal()
    conversation = create_conversation(db, text_request.text, text_request.question_id, text_request.order)
    process_text_task.delay(conversation.id)
    db.close()

    return conversation


@router.post("/send-text/", response_model=AudioResponse)
async def upload_text(text_message_request: TextMessageRequest):
    db = SessionLocal()
    audio = create_audio_by_text(db, text_message_request.text_message)
    process_text.delay(audio.id)
    db.close()

    return audio


@router.post("/upload-audio/", response_model=AudioResponse)
async def upload_audio(file: UploadFile):
    # Проверьте, что загруженный файл является .wav файлом, если это необходимо
    if not file.filename.endswith(".webm"):
        return {"error": "Можно загружать только .webm файлы."}
    # Генерируйте уникальное имя файла с использованием UUID
    unique_filename = str(uuid.uuid4()) + ".webm"
    file_path = os.path.join("uploads", unique_filename)
    # Сохраните файл на диск
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    # Сохраните информацию о файле в базе данных
    db = SessionLocal()
    audio = create_audio(db, unique_filename)
    process_audio.delay(audio.id)
    db.close()

    return audio


@router.get("/get_processed_text/{audio_id}", response_model=AudioResponse)
def get_processed_text(audio_id: int):
    db = SessionLocal()
    audio = get_audio_by_id(db, audio_id)
    db.close()
    if audio is None:
        raise HTTPException(status_code=404, detail="Audio not found")
    # Проверьте статус обработки аудио и верните результат
    if audio.question_text:
        return {
            "id": audio.id,
            "filename": audio.filename,
            "question_text": audio.question_text
        }
    else:
        raise HTTPException(status_code=404, detail="Audio is not processed yet")


@router.get("/get_answer/{answer_id}/{order}", response_model=ConversationResponse)
def create_conversation_endpoint(answer_id: int, order: int):
    db = SessionLocal()
    answer = get_answer_by_id(db, answer_id, order)
    db.close()
    if answer:
        return {
              "id": answer.id,
              "question_id": answer.question_id,
              "order": answer.order,
              "message_text": answer.message_text,
              "processed_status": answer.processed_status,
              "audio_link": answer.audio_link,
              "last_in_list": answer.last_in_list
            }
    else:
        raise HTTPException(status_code=404, detail="Ответ не найден")

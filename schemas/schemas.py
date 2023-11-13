from pydantic import BaseModel
from typing import Optional


class TextMessageRequest(BaseModel):
    text_message: str


class AudioResponse(BaseModel):
    id: int
    filename: Optional[str]
    question_text: Optional[str]


class ConversationResponse(BaseModel):
    id: int
    question_id: int
    order: int
    message_text: str
    processed_status: bool
    audio_link: Optional[str]
    last_in_list: bool


class TextRequest(BaseModel):
    text: str
    question_id: int
    order: int

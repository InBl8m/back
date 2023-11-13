import httpx
import json
import asyncio
from fastapi import WebSocket


async def websocket_exception_handler(request, exc):
    # Обработка ошибки WebSocketDisconnect
    print(f"WebSocketDisconnect: {exc}")
    return None


async def get_processed_text(data, max_attempts=20):
    for attempt in range(1, max_attempts + 1):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/get_processed_text/{data}")
            if response.status_code == 200:
                return response.text  # Возвращаем успешный результат
            else:
                if attempt < max_attempts:
                    # Если попытка не последняя, добавляем задержку перед следующей попыткой
                    await asyncio.sleep(1)
                else:
                    # Если попытка последняя, возвращаем None или подходящее значение для обозначения неудачи
                    return 'Нет ответа от сервера, или записи не существует'


async def get_answer(question_id, order, max_attempts=30):
    for attempt in range(1, max_attempts + 1):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/get_answer/{question_id}/{order}")
            if response.status_code == 200 and json.loads(response.text)["processed_status"] is True:
                return response.text  # Возвращаем успешный результат
            else:
                if attempt < max_attempts:
                    # Если попытка не последняя, добавляем задержку перед следующей попыткой
                    await asyncio.sleep(1)
                else:
                    # Если попытка последняя, возвращаем None или подходящее значение для обозначения неудачи
                    return '{"message_text": "Нет ответа от сервера, или записи не существует"}'


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data_json = await websocket.receive_text()
        try:
            data = json.loads(data_json)
            #  {"get_processed_text":69}
            if "get_processed_text" in data:
                print(data["get_processed_text"])
                processed_data = await get_processed_text(data["get_processed_text"])
                await websocket.send_text(processed_data)
            # {"get_answer":1, "order":1}
            elif "get_answer" in data:
                print('Запрашиваем ответ ', data)
                processed_data = await get_answer(data["get_answer"], data["order"])
                await websocket.send_text(processed_data)
            else:
                await websocket.send_text("wrong input")  # Отправляем "wrong input" при отсутствии или пустом поле
        except json.JSONDecodeError:
            await websocket.send_text("Invalid JSON format")

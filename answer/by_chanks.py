import openai
import requests


api_url = 'http://localhost:8000/process_text/'
openai.api_key = "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"
last_id = 0


def send_response(sentence, question_id, order):
    global last_id
    text_data = {
        "text": sentence,
        "question_id": question_id,
        "order": order
    }
    response = requests.post(api_url, json=text_data)

    # Проверка статуса ответа
    if response.status_code == 200:
        print("Запрос успешно отправлен.")
        response_data = response.json()  # Если API возвращает JSON, вы можете его распарсить
        print("Ответ от сервера:", response_data)
        last_id = response_data['id']
    else:
        print("Произошла ошибка при отправке запроса. Код статуса:", response.status_code)


def chat_generate(user_message, question_id):

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': user_message}
        ],
        temperature=0,
        stream=True  # this time, we set stream=True
    )

    sentence = ""
    order = 1
    for chunk in response:
        if 'content' in chunk['choices'][0]['delta']:
            chunk_content = chunk['choices'][0]['delta']['content']
            sentence += chunk_content
            if chunk_content.endswith('.') or chunk_content.endswith(',') or chunk_content.endswith('!'):
                # words = sentence.split(" ")
                send_response(sentence, question_id, order)
                sentence = ""
                order += 1
    if sentence:
        send_response(sentence, question_id, order)

    return last_id


if __name__ == "__main__":
    print(chat_generate("Расскажи про Марс, в пару предложений", 0))

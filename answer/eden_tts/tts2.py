import json
import os
import time
import requests


def text_to_speech(text='Привет друг!'):
    headers = {"Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                f"eyJ1c2VyX2lkIjoiYTg1OTU3ZDQtNDFjMy00NDNjLTlkMzgtYzBlMjg1YjFiMTNmIiwidHlwZSI"
                                f"6ImFwaV90b2tlbiJ9.MVredWdvzhwyulGPBvJQoQdKTEHYk5A-OsXNl86ved4"}
    url = 'https://api.edenai.run/v2/audio/text_to_speech'

    payload = {
        'providers': 'google',
        'language': 'ru-RU',
        # 'option': 'FEMALE',
        # 'lovoai': 'ru-RU_Anna Kravchuk',
        'option': 'MALE',
        'lovoai': 'ru-RU-Wavenet-D',
        'text': f'{text}'
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    unx_time = int(time.time())

    # with open(f'{unx_time}.json', 'w') as file:
    #     json.dump(result, file, indent=4, ensure_ascii=False)

    audio_url = result.get('google').get('audio_resource_url')
    r = requests.get(audio_url)
    file_name = f'{unx_time}.wav'
    audio_folder = 'answer/audio'
    # Создайте полный путь к файлу
    file_path = os.path.join(audio_folder, file_name)
    with open(file_path, 'wb') as file:
        file.write(r.content)
    return file_path


if __name__ == '__main__':
    text_to_speech("Привет как дела")

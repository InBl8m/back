import os
import speech_recognition as sr
from pydub import AudioSegment


# Функция для конвертации аудио из webm в WAV
def convert_webm_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file, format="webm")
    audio.export(output_file, format="wav")


def get_question(webm_file):
    audio_file = webm_file[:-4] + "wav"
    # Конвертируем webm в WAV
    convert_webm_to_wav(webm_file, audio_file)
    # Создаем объект Recognizer
    recognizer = sr.Recognizer()
    # Загружаем аудиофайл
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    # Проводим распознавание текста с помощью Google
    try:
        recognized_text = recognizer.recognize_google(audio_data, language="ru-RU")
        print("Распознанный текст: " + recognized_text)
        return recognized_text
    except sr.UnknownValueError:
        return "Голос не распознан"
    except sr.RequestError as e:
        print("Ошибка при отправке запроса к сервису Google: {0}".format(e))

    # os.remove(webm_file)


if __name__ == "__main__":
    get_question('../uploads/1383f447-1f49-4d63-9573-a021c3067871.webm')

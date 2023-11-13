import os
import uuid
from gtts import gTTS


def text_to_speech(sentence):
    print(sentence)
    tts = gTTS(sentence, lang='ru')
    unique_filename = str(uuid.uuid4()) + '.mp3'
    output_path = os.getcwd() + '/uploads/answers/' + unique_filename
    print(output_path)
    tts.save(output_path)
    return unique_filename


if __name__ == "__main__":
    text_to_speech('Привет, киты большие')

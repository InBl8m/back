from pydub import AudioSegment
from pydub.playback import play


def play_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    play(audio)


if __name__ == '__main__':
    audio_file_path = f"{1697659221}.wav"  # Replace with the actual path to your audio file
    play_audio(audio_file_path)

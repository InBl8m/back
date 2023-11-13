import wave

# Укажите путь к вашему .wav файлу
audio_file_path = 'output.wav'

try:
    # Откройте файл в бинарном режиме
    with open(audio_file_path, 'rb') as file:
        # Считайте первые 4 байта (RIFF идентификатор)
        riff_id = file.read(4)

        # Выведите идентификатор RIFF
        print("RIFF идентификатор:", riff_id)
except Exception as e:
    print("Произошла ошибка при чтении файла:", e)

import subprocess
import argparse
import os

### Работающая версия обработки видео
def get_video_resolution(input_file):
    """
    Получает разрешение видео (ширину и высоту) с помощью FFmpeg.
    """
    # Команда FFmpeg для получения информации о видео
    command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=s=x:p=0',
        input_file
    ]

    # Выполнение команды
    try:
        output = subprocess.check_output(command).decode('utf-8').strip()
        width, height = map(int, output.split('x'))
        return width, height
    except subprocess.CalledProcessError:
        return None, None


def convert_video(input_file, resolutions):
    """
    Конвертирует видео в различные разрешения с использованием FFmpeg.

    input_file: путь к входному видеофайлу.
    resolutions: словарь с разрешениями для каждой ориентации.
    """
    # Получение разрешения видео
    width, height = get_video_resolution(input_file)

    if width is None or height is None:
        print("Не удалось получить разрешение видео.")
        return

    # Извлечение имени файла и расширения
    file_name, file_extension = os.path.splitext(input_file)

    # Определение ориентации видео
    if width >= height:
        orientation = 'horizontal'
    else:
        orientation = 'vertical'

    # Выбор разрешений в зависимости от ориентации
    target_resolutions = resolutions.get(orientation, {})

    # Перебор разрешений и конвертация видео
    for resolution, height in target_resolutions.items():
        # Формирование имени выходного файла
        output_file = f"{file_name}_{resolution}p{file_extension}"

        # Команда FFmpeg для конвертации видео в указанное разрешение
        command = [
            'ffmpeg',
            '-i', input_file,
            '-vf', f'scale={resolution}:{height}',  # Масштабирование до указанного разрешения
            '-c:a', 'copy',  # Копирование аудиопотока без изменений
            output_file
        ]

        # Выполнение команды
        try:
            subprocess.run(command, check=True)
            print(f"Видео успешно конвертировано в {resolution}p и сохранено как {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при конвертации видео: {e}")


if __name__ == "__main__":
    # Создание парсера аргументов командной строки
    parser = argparse.ArgumentParser(description='Конвертацмя видео в различные разрешения')
    parser.add_argument('input_file', help='Путь к входному видео')

    # Парсинг аргументов
    args = parser.parse_args()

    # Разрешения для каждой ориентации
    resolutions = {
        'horizontal': {'720': 720, '480': 480, '360': 360},
        'vertical': {'720': 406, '480': 270, '360': 202}
    }

    # Конвертирование видео
    convert_video(args.input_file, resolutions)
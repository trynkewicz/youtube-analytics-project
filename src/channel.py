import os
import json
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""

    #api_key: str = os.getenv('YT_API_KEY')
    #youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

        api_key = os.getenv('YT_API_KEY')

        if not api_key:
            raise ValueError("API-ключ YouTube не найден. "
                             "Установите переменную окружения YT_API_KEY.")

        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        response = self.youtube.channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()

        print(json.dumps(response, indent=2, ensure_ascii=False))

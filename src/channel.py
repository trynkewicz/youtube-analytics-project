import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для YouTube-канала"""

    def __init__(self, channel_id: str) -> None:
        """Инициализация канала и получение данных через API"""
        self._channel_id = channel_id  # readonly атрибут

        api_key = os.getenv('YT_API_KEY')
        if not api_key:
            raise ValueError(
                "API-ключ YouTube не найден. Установите переменную окружения YT_API_KEY."
            )

        # создаем объект для работы с YouTube API
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self._load_channel_data()

    # ----------------- readonly properties -----------------
    @property
    def channel_id(self):
        return self._channel_id

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def url(self):
        return f"https://www.youtube.com/channel/{self.channel_id}"

    @property
    def subscriber_count(self):
        return self._subscriber_count

    @property
    def video_count(self):
        return self._video_count

    @property
    def view_count(self):
        return self._view_count

    # ----------------- private methods -----------------
    def _load_channel_data(self):
        """Заполняет атрибуты экземпляра данными канала через API"""
        response = self.youtube.channels().list(
            id=self.channel_id,
            part="snippet,statistics"
        ).execute()

        if not response['items']:
            raise ValueError(f"Канал с id={self.channel_id} не найден")

        item = response['items'][0]
        snippet = item['snippet']
        stats = item['statistics']

        self._title = snippet.get('title', '')
        self._description = snippet.get('description', '')
        self._subscriber_count = int(stats.get('subscriberCount', 0))
        self._video_count = int(stats.get('videoCount', 0))
        self._view_count = int(stats.get('viewCount', 0))

    # ----------------- public methods -----------------
    def print_info(self) -> None:
        """Выводит данные канала в удобном формате"""
        info = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        print(json.dumps(info, indent=2, ensure_ascii=False))

    def to_json(self, filename: str) -> None:
        """Сохраняет данные канала в JSON-файл"""
        info = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(info, f, indent=2, ensure_ascii=False)

    # ----------------- class methods -----------------
    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key = os.getenv('YT_API_KEY')
        if not api_key:
            raise ValueError(
                "API-ключ YouTube не найден. Установите переменную окружения YT_API_KEY."
            )
        return build('youtube', 'v3', developerKey=api_key)

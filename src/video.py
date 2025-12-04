import os
import json
from googleapiclient.discovery import build

# Создаем объект для работы с YouTube API
api_key = os.getenv('YT_API_KEY')
if not api_key:
    raise ValueError("API-ключ YouTube не найден. Установите переменную окружения YT_API_KEY.")

youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """Класс для работы с YouTube видео"""

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self._load_video_data()

    def _load_video_data(self):
        """Получаем данные о видео через API"""
        response = youtube.videos().list(
            part="snippet,statistics",
            id=self.video_id
        ).execute()

        if not response['items']:
            raise ValueError(f"Видео с id={self.video_id} не найдено")

        item = response['items'][0]
        snippet = item['snippet']
        stats = item['statistics']

        self.title = snippet.get('title', '')
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.view_count = int(stats.get('viewCount', 0))
        self.like_count = int(stats.get('likeCount', 0))

    def __str__(self):
        return self.title


class PLVideo(Video):
    """Класс видео, привязанного к плейлисту"""

    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
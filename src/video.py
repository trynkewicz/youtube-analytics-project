import os
from googleapiclient.discovery import build

api_key = os.getenv("YT_API_KEY")
if not api_key:
    raise ValueError("Не найден API ключ YT_API_KEY")

youtube = build("youtube", "v3", developerKey=api_key)


class Video:
    """Класс для работы с YouTube-видео"""

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.title = None
        self.url = None
        self.view_count = None
        self.like_count = None

        try:
            response = youtube.videos().list(
                id=self.video_id,
                part="snippet,statistics"
            ).execute()

            if not response["items"]:
                # видео с таким ID нет → оставляем None
                return

            item = response["items"][0]

            self.title = item["snippet"]["title"]
            self.url = f"https://youtu.be/{self.video_id}"
            self.view_count = int(item["statistics"].get("viewCount", 0))
            self.like_count = int(item["statistics"].get("likeCount", 0))

        except Exception:
            # Любая ошибка API → оставляем только video_id
            pass


class PLVideo(Video):
    """Видео, находящееся в плейлисте"""

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id

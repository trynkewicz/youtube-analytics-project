import os
from datetime import timedelta
from googleapiclient.discovery import build
import isodate


# YouTube API
api_key = os.getenv("YT_API_KEY")
if not api_key:
    raise ValueError("Не найден API ключ YT_API_KEY")

youtube = build("youtube", "v3", developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id

        playlist_response = youtube.playlists().list(
            id=self.playlist_id,
            part="snippet"
        ).execute()

        playlist = playlist_response["items"][0]["snippet"]
        self.title = playlist["title"]
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

        # ID всех видео внутри плейлиста
        self.video_ids = self._get_video_ids()

    def _get_video_ids(self):
        """Собирает ID всех видео плейлиста (учитывает многостраничность)."""
        ids = []
        next_page = None

        while True:
            response = youtube.playlistItems().list(
                playlistId=self.playlist_id,
                part="contentDetails",
                maxResults=50,
                pageToken=next_page
            ).execute()

            ids.extend(item["contentDetails"]["videoId"] for item in response["items"])

            next_page = response.get("nextPageToken")
            if not next_page:
                break

        return ids

    @property
    def total_duration(self):
        """Возвращает суммарную длительность всех видео в плейлисте."""
        total = timedelta()

        video_response = youtube.videos().list(
            id=",".join(self.video_ids),
            part="contentDetails"
        ).execute()

        for video in video_response["items"]:
            iso_duration = video["contentDetails"]["duration"]
            duration = isodate.parse_duration(iso_duration)
            total += duration

        return total

    def show_best_video(self):
        """Возвращает ссылку на видео с максимальным количеством лайков."""
        videos_response = youtube.videos().list(
            id=",".join(self.video_ids),
            part="statistics"
        ).execute()

        best_video_id = None
        best_likes = -1

        for video in videos_response["items"]:
            likes = int(video["statistics"].get("likeCount", 0))
            if likes > best_likes:
                best_likes = likes
                best_video_id = video["id"]

        return f"https://youtu.be/{best_video_id}"

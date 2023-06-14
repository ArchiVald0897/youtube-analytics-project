import os
from googleapiclient.discovery import build


class Video:
    """Класс для ютуб-канала"""

    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv("YT_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video_i = self.youtube.videos().list(id=video_id, part="snippet,statistics").execute()

    @property
    def title(self):
        return self.video_i["items"][0]["snippet"]["title"]

    @property
    def url(self):
        return f'https://www.youtube.com/watch?v={self.video_id}'

    @property
    def view_count(self):
        return self.video_i["items"][0]["statistics"]["viewCount"]

    @property
    def like_count(self):
        return self.video_i["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        return self.title


class PLVideo(Video):
    """Класс для видио с ютьюб-канала в плейлистах"""

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return self.title

from googleapiclient.errors import HttpError

from src.channel import YouTubeAPI


class Video(YouTubeAPI):
    """Класс для ютуб-канала"""

    def __init__(self, video_id: str):
        self.video_id = video_id
        try:
            self.video_i = self.youtube.videos().list(id=video_id, part="snippet,statistics").execute()
        except HttpError:
            self.video_i = {"items": [{}]}

    @property
    def title(self):
        return self.video_i["items"][0]["snippet"]["title"] if self.video_i["items"] else None

    @property
    def url(self):
        return f'https://www.youtube.com/watch?v={self.video_id}'

    @property
    def view_count(self):
        return self.video_i["items"][0]["statistics"]["viewCount"] if self.video_i["items"] else None

    @property
    def like_count(self):
        return self.video_i["items"][0]["statistics"]["likeCount"] if self.video_i["items"] else None

    def __str__(self):
        return self.title or ""


class PLVideo(Video):
    """Класс для видео с ютьюб-канала в плейлистах"""

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        try:
            self.playlist_info = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                   part='contentDetails',
                                                                   maxResults=50).execute()
        except HttpError:
            self.playlist_info = {"items": []}

    def __str__(self):
        return self.title or ""

from src.channel import YouTubeAPI


class Video(YouTubeAPI):
    """Класс для ютуб-канала"""

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
        self.playlist_info = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                               part='contentDetails',
                                                               maxResults=50).execute()

    def __str__(self):
        return self.title

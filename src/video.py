from googleapiclient.errors import HttpError

from src.channel import YouTubeAPI


class Video(YouTubeAPI):
    """Класс для ютуб-канала"""

    def __init__(self, video_id: str):
        self._video_id = video_id
        try:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=video_id).execute()

            self.video_title: str = video_response['items'][0]['snippet']['title']
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
            self.comment_count: int = video_response['items'][0]['statistics']['commentCount']
            self.video_url: str = f'https://youtu.be/{self._video_id}'
        except Exception:
            self.video_title = None
            self.view_count = None
            self.like_count = None
            self.comment_count = None
            self.video_url = None

    def __str__(self):
        return f"{self.video_title}"


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
        return f"{self.video_title}"



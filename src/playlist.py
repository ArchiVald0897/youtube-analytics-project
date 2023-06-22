import datetime
from src.video import Video
import os
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv("YT_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id

    @property
    def title(self):
        # Получаем информацию о плейлисте и возвращаем его название
        playlist_info = self.youtube.playlists().list(id=self.playlist_id, part="snippet").execute()
        return playlist_info["items"][0]["snippet"]["title"]

    @property
    def url(self):
        # Возвращаем ссылку на плейлист
        return f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def total_duration(self):
        # Получаем информацию о видео в плейлисте
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        total_seconds = 0
        # Считаем общую продолжительность всех видео в плейлисте
        for item in playlist_videos["items"]:
            video_id = item["contentDetails"]["videoId"]
            video_duration = self.youtube.videos().list(id=video_id,
                                                        part="contentDetails"
                                                        ).execute()["items"][0]["contentDetails"]["duration"]
            duration_seconds = duration_to_seconds(video_duration)
            total_seconds += duration_seconds
        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        # Находим видео с наибольшим количеством лайков в плейлисте
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='snippet',
                                                            maxResults=50,
                                                            ).execute()
        max_likes = 0
        best_video_url = ""
        for item in playlist_videos["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            video = Video(video_id)
            likes = int(video.like_count)
            if likes > max_likes:
                max_likes = likes
                best_video_url = video.url
        return best_video_url


def duration_to_seconds(duration):
    """Функция для конвертирования длительности видео в секунды"""
    duration_str = duration.replace("PT", "").lower()
    seconds = 0
    if "h" in duration_str:
        hours, duration_str = duration_str.split("h")
        seconds += int(hours) * 3600
    if "m" in duration_str:
        minutes, duration_str = duration_str.split("m")
        seconds += int(minutes) * 60
    if "s" in duration_str:
        seconds += int(duration_str[:-1])
    return seconds

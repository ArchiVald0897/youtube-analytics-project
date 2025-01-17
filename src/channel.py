import json
import os
from googleapiclient.discovery import build


class YouTubeAPI:
    """Класс для ютуб-канала"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv("YT_API_KEY")
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)


class Channel(YouTubeAPI):

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel_info = self.youtube.channels().list(id=self.channel_id, part="snippet,statistics").execute()
        self.title = self.channel_info["items"][0]["snippet"]["title"]
        self.description = self.channel_info["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscribers_count = self.channel_info["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel_info["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel_info["items"][0]["statistics"]["viewCount"]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.title}(https://www.youtube.com/channel/{self.url}))"

    def __str__(self):
        return f"{self.title}{self.url}"

    def __add__(self, other):
        """суммируем количество подписчиков"""
        return int(self.subscribers_count) + int(other.subscribers_count)

    def __sub__(self, other):
        """вычитае количество подписчиков"""
        return int(self.subscribers_count) - int(other.subscribers_count)

    def __lt__(self, other):
        return int(self.subscribers_count) < int(other.subscribers_count)

    def __gt__(self, other):
        return int(self.subscribers_count) > int(other.subscribers_count)

    def __le__(self, other):
        return int(self.subscribers_count) <= int(other.subscribers_count)

    def __ge__(self, other):
        return int(self.subscribers_count) >= int(other.subscribers_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале в формате JSON"""
        channel = self.youtube.channels().list(id=self.channel_id, part="snippet,statistics").execute()
        channel_json = json.dumps(channel, indent=2, ensure_ascii=False)
        print(channel_json)

    @classmethod
    def get_service(cls):
        return cls.youtube

    @property
    def channel_id(self):
        return self.__channel_id

    def to_json(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.__dict__, file, ensure_ascii=False)

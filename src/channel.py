import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv("YT_API_KEY")
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel_i = self.youtube.channels().list(id=self.channel_id, part="snippet,statistics").execute()
        self.title = self.channel_i["items"][0]["snippet"]["title"]
        self.description = self.channel_i["items"][0]["snippet"]["description"]
        self.url = self.get_channel_self()
        self.subscribers_count = self.channel_i["item"][0]["statistics"]["subscriberCount"]
        self.vidio_count = self.channel_i["item"][0]["statistics"]["videoCount"]
        self.view_count = self.channel_i["item"][0]["statistics"]["viewCount"]

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

    def get_channel(self):
        return f"https://www.youtube.com/channel/{self.channel_id}"

    def to_json(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dumps(self.__dict__, f, ensure_ascii=False)


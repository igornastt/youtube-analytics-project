import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""
    channel_info = None
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.channel_id = channel_id

        channel = Channel.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']['thumbnails']["default"]['url']
        self.subscriberCount = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.views_count = channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.channel_info = json.dumps(channel, indent=2, ensure_ascii=False)
        return self.channel_info

    @classmethod
    def get_service(cls):
        '''
         Возвращает объект для работы с YouTube API
         '''
        api_key: str = os.getenv('YT_API_KEY')
        object_get = build('youtube', 'v3', developerKey=api_key)
        return object_get

    def to_json(self, filename):
        '''
        Сохраняет в файл значения атрибутов экземпляра Channel
        '''
        dict_hom = {}

        dict_hom['id'] = self.channel_id
        dict_hom['title'] = self.title
        dict_hom['description'] = self.description
        dict_hom['url'] = self.url
        dict_hom['subscriberCount'] = self.subscriberCount
        dict_hom['video_count'] = self.video_count
        dict_hom['views_count'] = self.views_count

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dict_hom, f, indent=2)

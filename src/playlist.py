import isodate
from datetime import timedelta
import os
from googleapiclient.discovery import build
from src.video import PLVideo


class PlayList:
    """
    Класс для плейлистов ютуб. Инициализируется по id плейлиста.
    """
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:
        """Конструктор класса PlayList"""
        self.playlist_id = playlist_id
        self.playlist_response = self.youtube.playlists().list(id=playlist_id,
                                                               part='snippet, contentDetails').execute()
        self.playlist_items = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                part='snippet, contentDetails').execute()
        self.title = self.playlist_response["items"][0]["snippet"]["title"]
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.playlist_videos = self.__private_load_videos()

    def __private_load_videos(self) -> list[PLVideo]:
        """
        Функция загрузки данных о видео плейлиста.
        Возвращает список экземпляров класса PLVideo.
        """
        load_video = []
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_items['items']]
        for video_id in self.video_ids:
            load_video.append(PLVideo(video_id, self.playlist_id))
        return load_video

    @property
    def total_duration(self):
        """
        Функция вычисляет суммарную длительность видео плейлиста.
        """
        total_duration = timedelta()
        for video in self.playlist_videos:
            duration = isodate.parse_duration(video.duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """
        Функция для определения самого популярного видео в плейлисте.
        Возвращает ссылку на видео.
        """
        like_max = 0
        best_video = None
        for video in self.playlist_videos:
            if int(video.like_count) > like_max:
                best_video = video
        return best_video.url
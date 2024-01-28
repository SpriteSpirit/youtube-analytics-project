from datetime import timedelta
from src.channel import Channel
from src.video import Video
import re


class PlayList:
    video_ids = []
    nextPageToken = None
    service = Channel.get_service()

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = None
        self.url = f'https: //www.youtube.com/playlist?list={self.playlist_id}'
        self._total_duration = None

    @property
    def total_duration(self):
        """
        Геттер общей продолжительности плейлиста.
        :return:
        """
        if self._total_duration is None:
            self.get_videos_and_duration()
        return self._total_duration

    def get_playlist_info(self):
        """
        Получает расширенную информацию о плейлисте через API,
        обращаясь к Youtube Data API.
        :return: Словарь с информацией по плейлисту
        """
        request = self.service.playlists().list(
            part='snippet',
            id=self.playlist_id
        )

        return request.execute()

    def get_videos_and_duration(self):
        pass
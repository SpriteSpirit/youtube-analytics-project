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
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self._title = None
        self._total_duration = None
        # self.get_videos_and_duration()

    @property
    def title(self):
        if self._title is None:
            self._title = self.get_playlist_info()['items'][0]['snippet']['title']
        return self._title

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

    def get_playlist_items(self):
        """
        Возвращает словарь с информацией по видео из плейлиста.
        """
        response = self.service.playlistItems().list(
            part='contentDetails, snippet',
            playlistId=self.playlist_id,
            maxResults=50,
            pageToken=self.nextPageToken
        ).execute()

        return response

    def get_videos_and_duration(self):
        """
        Получает продолжительность всех видео и подсчитывает суммарное время продолжительности.
        :return:
        """

        hours_pattern = re.compile(r'(\d+)H')
        minutes_pattern = re.compile(r'(\d+)M')
        seconds_pattern = re.compile(r'(\d+)S')

        total_duration = timedelta()

        while True:
            vid_items = self.get_playlist_items()

            for item in vid_items.get('items', []):
                video_id = item['contentDetails']['videoId']
                self.video_ids.append(video_id)

            video_response = Video.get_video_info(','.join(self.video_ids))

            for item in video_response['items']:
                duration = item['contentDetails']['duration']

                hours = hours_pattern.search(duration)
                minutes = minutes_pattern.search(duration)
                seconds = seconds_pattern.search(duration)

                hours = int(hours.group(1)) if hours else 0
                minutes = int(minutes.group(1)) if minutes else 0
                seconds = int(seconds.group(1)) if seconds else 0

                video_duration = timedelta(
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds
                )

                total_duration += video_duration

            self.nextPageToken = vid_items.get('nextPageToken')

            if not self.nextPageToken:
                break

        self._total_duration = total_duration

    def show_best_video(self):
        """
        Находит максимальное кол-во лайков у видео и определяет id видео
        :return:
        """
        best_video_id = None
        best_video_likes = 0

        for video in self.video_ids:
            response = Video.get_video_info(video)
            likes_count = int(response.get('items', [])[0]['statistics']['likeCount'])

            if likes_count > best_video_likes:
                best_video_likes = likes_count
                best_video_id = video

        if best_video_id:
            return f'https://youtu.be/{best_video_id}'
        else:
            return None

from src.channel import Channel


class Video:
    service = Channel.get_service()

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video_title = self.get_video_info()['items'][0]['snippet']['title']
        self.video_url = f'https://www.youtube.com/watch?v={self.video_id}'
        self.view_count = self.get_video_info()['items'][0]['statistics']['viewCount']
        self.like_count = self.get_video_info()['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.video_title}'

    def get_video_info(self) -> dict:
        """
        Получает расширенную информацию о видео через API,
        обращаясь к Youtube Data API.
        :return:  Возвращает словарь с указанными данными о видео
        """
        request = self.service.videos().list(part='snippet, statistics', id=self.video_id)
        response = request.execute()

        return response


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id


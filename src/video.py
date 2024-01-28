from src.channel import Channel


class Video:
    service = Channel.get_service()

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.items = Video.get_video_info(self.video_id)['items'][0]
        self.video_title = self.items['snippet']['title']
        self.video_url = f'https://www.youtube.com/watch?v={self.video_id}'
        self.view_count = self.items['statistics']['viewCount']
        self.like_count = self.items['statistics']['likeCount']

    def __str__(self):
        return f'{self.video_title}'

    @classmethod
    def get_video_info(cls, vid_id) -> dict:
        """
        Получает расширенную информацию о видео через API,
        обращаясь к Youtube Data API.
        :return:  Возвращает словарь с указанными данными о видео
        """
        request = cls.service.videos().list(part='snippet, contentDetails, statistics', id=vid_id)
        response = request.execute()

        return response


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id


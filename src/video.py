from src.channel import Channel


class Video:
    service = Channel.get_service()

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video_title = None
        self.video_url = None
        self.view_count = None
        self.like_count = None

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

import os

from googleapiclient.discovery import build
class Video:

    def __init__(self, video_id):
        self.video_id = video_id
        video_response = Video.get_service().videos().list(part='snippet,contentDetails,statistics',
                                               id=video_id).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']

    def __repr__(self):
        return f"{self.__class__.__name__} ('{self.video_id}','{self.video_title}',{self.view_count},{self.like_count},{self.comment_count})"
    def __str__(self):
        """возвращаем титл видео"""
        return f"{self.video_title}"

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube
class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __repr__(self):
        return f"{self.__class__.__name__} ('{self.video_id}','{self.video_title}',{self.view_count},{self.like_count},{self.comment_count}, '{self.playlist_id}')"
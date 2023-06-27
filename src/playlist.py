import os
import datetime
from datetime import timedelta
import isodate
from googleapiclient.discovery import build

class PlayMixin:
    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

class PlayList(PlayMixin):
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id

        self.title: str = self.get_info()['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    def __repr__(self):
        return f"{self.__class__.__name__} ('{self.playlist_id}','{self.title}','{self.url}')"

    def __call__(self, *args, **kwargs):
        pass

    def get_info(self):
        playlists = PlayList.get_service().playlists().list(
            part="contentDetails,snippet",
            id=self.playlist_id
        ).execute()
        return playlists


    @property
    def total_duration(self):
        playlists = self.get_pl_video()
        timeline = []
        for video in playlists['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            timeline.append(duration)
        result = sum(timeline, timedelta())
        return result

    def show_best_video(self):
        playlists = self.get_pl_video()
        best_video = 0
        top_video_url = ""
        for top in playlists['items']:
            best = top['statistics']['likeCount']
            if int(best) > int(best_video):
                best_video = best
                top_video_url = top['id']
        return f'https://youtu.be/{top_video_url}'

    def get_pl_video(self):
        playlist_videos = PlayList.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                              id=','.join(video_ids)).execute()

        return video_response

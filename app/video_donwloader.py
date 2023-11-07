"""video downloader
"""
import dataclasses
import os
import re
from typing import List, TypedDict

from pytube import Search, YouTube


class YTVideo(TypedDict):
    """class YTVideo dict
    """
    video_id: str
    title: str
    interpret: str
    length: float
    url: str
    video_title: str
    yt_video: YouTube


@dataclasses.dataclass
class VideoDownloader:
    """Video class
    """
    username: str
    video_path: str = "data/video/"

    def __post_init__(self):
        self.video_path = os.path.join(self.video_path, self.username.lower())

    def download_by_id(self, video_id: str) -> str:
        """Download youtube video from url
        """
        url: str = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(url)
        filename = self.generate_outfile_name(filename=yt.title)
        yt.streams.filter(
            progressive=True,
            file_extension="mp4",
        ).order_by(
            "resolution",
        ).desc().first().download(
            filename=filename,
        )

        return filename

    def generate_outfile_name(self, filename: str) -> str:
        """Remove whitespaces from filename
        """
        filename = re.sub(r"\W+", "_", filename).strip("_")

        return os.path.join(self.video_path, filename)

    def search(self, interpret: str, title: str) -> List[YTVideo]:
        """Search youtube videos
        """
        query = f"{interpret} {title}"
        videos = []
        yt_search = Search(query=query)
        videos = [
            YTVideo(
                title=title,
                interpret=interpret,
                video_id=video.video_id,
                length=video.length / 60,
                url=video.watch_url,
                video_title=video.title,
                yt_video=video,
            ) for video in yt_search.results
        ]

        return videos

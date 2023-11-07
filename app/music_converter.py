"""Music converter
"""
import dataclasses
import os
import shutil
from typing import List

import moviepy.editor as mp


@dataclasses.dataclass
class MusicConverter:
    """Converter"""

    username: str
    video_path: str = "data/video/"
    music_path: str = "data/music/"

    def __post_init__(self):
        self.video_path = os.path.join(self.video_path, self.username.lower())
        self.music_path = os.path.join(self.music_path, self.username.lower())

    def _convert(self, infile: str, outfile: str):
        """Convert from video to music"""
        clip = mp.VideoFileClip(filename=infile)
        clip.audio.write_audiofile(filename=outfile)

    def _convert_video_files(self):
        """Convert video to mp4"""
        files_without_ext = [
            os.path.splitext(filename)
            for filename in os.listdir(self.video_path)
            if os.path.splitext(filename)[1] != ".mp4"
        ]

        for filename in files_without_ext:
            shutil.move(
                self.video_path + "/" + filename[0] + filename[1],
                self.video_path + "/" + filename[0] + ".mp4",
            )

    def _generate_outfile_path(self, filepath: str) -> str:
        """Generate outfile path"""
        filename = os.path.split(filepath)[1] + ".mp3"

        return os.path.join(self.music_path, filename)

    def convert(self, video_files: List[str]):
        """convert video to music"""
        self._convert_video_files()

        for filename in video_files:
            if filename.startswith("."):
                continue
            outfile = self._generate_outfile_path(filepath=filename)

            if not os.path.exists(outfile):
                self._convert(infile=filename, outfile=outfile)

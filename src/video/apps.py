from django.apps import AppConfig
from django.core.checks import register

from .checks import check_ffmpeg


class VideoConfig(AppConfig):
    name = 'video'

    def ready(self):
        register(check_ffmpeg, self.name)

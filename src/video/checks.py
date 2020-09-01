from shutil import which

from django.core.checks import Error


def check_ffmpeg(app_configs, **kwargs):
    errors = []
    if not which('ffmpeg'):
        errors.append(
            Error(
                'A executable file `ffmpeg` doesn\'t installed.',
                hint='Please install `ffmpeg` package.',
                id='video.E001',
            )
        )
    return errors

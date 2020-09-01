import uuid

from functools import partial
from pathlib import Path

from django.conf import settings
from django.db import models
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

from .validators import validate_video_file_extension


def get_adjusted_filename(instance, filename, upload_to, file_type):
    return (
        Path(upload_to) / Path(instance.original_file.name).stem
    ).with_suffix(f'.{file_type}')


class VideoFile(models.Model):

    DEFAULT_PREVIEW_IMAGE_URL = static(
        getattr(
            settings,
            'DEFAULT_PREVIEW_IMAGE',
            'images/default.png',
        )
    )

    original_file = models.FileField(
        blank=True,
        upload_to='video/original/',
        verbose_name=_('original uploaded file'),
        validators=[
            validate_video_file_extension
        ],
    )

    url = models.URLField(
        blank=True,
        verbose_name=_('URL of file for uploading'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        verbose_name=_('UUID'),
    )

    preview = models.ImageField(
        upload_to=partial(
            get_adjusted_filename,
            upload_to='images/preview/',
            file_type='jpg',
        ),
        blank=True,
        verbose_name=_('preview'),
    )

    # Maybe these fields are better placed in a separated model?
    # But it's the simplest way. Simple is better than complex.
    # Let's do it!
    video_as_mp4 = models.FileField(
        upload_to=partial(
            get_adjusted_filename,
            upload_to='video/mp4/',
            file_type='mp4',
        ),
        blank=True,
        verbose_name=_('MP4 video file'),
    )

    video_as_webm = models.FileField(
        upload_to=partial(
            get_adjusted_filename,
            upload_to='video/webm/',
            file_type='webm',
        ),
        blank=True,
        verbose_name=_('WEBM video file'),
    )

    class Meta:
        verbose_name = _('video file')
        verbose_name_plural = _('video files')

    @property
    def preview_url(self):
        """Return URL for preview if ready or default image URL."""
        if self.preview:
            return self.preview.url
        return VideoFile.DEFAULT_PREVIEW_IMAGE_URL

    def get_media_field(self, file_type):
        file_type_to_field = {
            'jpg': self.preview,
            'mp4': self.video_as_mp4,
            'webm': self.video_as_webm,
        }
        try:
            return file_type_to_field[file_type]
        except KeyError:
            raise KeyError(f'Unknown file type: `{file_type}`.')

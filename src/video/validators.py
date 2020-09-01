from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


VALID_UPLOAD_EXTENSIONS = getattr(
    settings,
    'VALID_UPLOAD_EXTENSIONS',
    ['.avi', '.mp4', '.webm', '.mov'],
)


def validate_video_file_extension(value):
    """Validate video extension of filename."""
    extension = Path(value.name).suffix
    if extension.lower() not in VALID_UPLOAD_EXTENSIONS:
        raise ValidationError(_('Unsupported file extension.'))

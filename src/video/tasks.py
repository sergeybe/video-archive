import tempfile
import celery
from celery.canvas import group

import requests
import shutil

from pathlib import Path
from urllib.parse import urlparse

from django.conf import settings
from django.core.files import File

from celery import shared_task
from celery.utils.log import get_task_logger

from .encoding import encode_video_file
from .models import VideoFile

logger = get_task_logger('video.tasks')


def process_video_file(video_file):
    """Process video file."""

    if video_file.url:
        download_file.delay(video_file.id, process=True)
    elif video_file.original_file:
        celery.group(
            create_preview.s(video_file.id),
            encode_video_to_mp4.s(video_file.id),
            encode_video_to_webm.s(video_file.id),
        ).delay()
    else:
        logger.error(
            'No data for encoding in video file: %s',
            video_file.id
        )


@shared_task
def encode_video(video_file_id: int, file_type: str):
    logger.info(
        'Start encoding for %d, video format: %s',
        video_file_id,
        file_type,
    )

    try:
        video_file = (
            VideoFile.objects.get(id=video_file_id)
        )
    except VideoFile.DoesntExists:
        logger.error('Video file %s doesn\'t exists.')
        return

    if file_type not in settings.VIDEO_FORMATS:
        logger.error('Video format `%s` doesn\t supported!')
        return

    temp_file_path = Path(
        tempfile.mktemp(
            prefix='video',
            suffix=f'.{file_type}',  # Must be with extension for ffmpeg.
        )
    )

    returncode = encode_video_file(
        video_file.original_file.path,
        temp_file_path,
        file_type,
    )

    if returncode == 0:
        with temp_file_path.open(mode='rb') as f:
            field = video_file.get_media_field(file_type)
            field.save('', File(f), save=False)
            video_file.save(
                force_update=True,
                update_fields=[field.field.name],
            )
    else:
        logger.error(
            'Can\t enocode file id %d, file type: %s',
            video_file_id,
            file_type,
        )

    temp_file_path.unlink()
    logger.info(
        'End encoding has for %s', video_file_id
    )
    return video_file_id


@shared_task
def encode_all_videos(video_file_id: int):
    try:
        video_file = VideoFile.objects.get(id=video_file_id)
    except VideoFile.DoesntExists:
        logger.error(
            'Video file %s doesn\'t exists.',
            video_file_id
        )
        return

    video_formats = getattr(
        settings,
        'VIDEO_FORMATS',
        []
    )

    for video_format in video_formats:
        # If video format was encoded yet.
        media_field = video_file.get_media_field(video_format)
        if media_field:
            continue
        encode_video(video_file.id, video_format)
    return video_file_id


@shared_task
def create_preview(video_file_id: int):
    """Task to create preview image."""
    return encode_video(video_file_id, 'jpg')


@shared_task
def encode_video_to_mp4(video_file_id: int):
    """Task to encode video to mp4."""
    return encode_video(video_file_id, 'mp4')


@shared_task
def encode_video_to_webm(video_file_id: int):
    """Task to encode video to webm."""
    return encode_video(video_file_id, 'webm')


@shared_task
def download_file(video_file_id: int, process: bool = False):
    try:
        video_file = (
            VideoFile.objects.get(id=video_file_id)
        )
    except VideoFile.DoesntExists:
        logger.error(
            'Video file #%s doesn\'t exists.',
            video_file_id,
        )
        return

    if not video_file.url:
        logger.error(
            'Video file #%s hasn\'t url.',
            video_file_id
        )
        return

    if video_file.original_file:
        logger.error(
            'The original file is set for video file #%s.',
            video_file_id,
        )

    # TODO: We will support only urls with file extensions.
    # It's more complexly but not so difficult.

    parse_result = urlparse(video_file.url)

    if parse_result.scheme not in ['https', 'http']:
        logger.error('Support only http and https schemas.')
        return

    file_name = Path(parse_result.path)

    temp_file_path = Path(
        tempfile.mktemp(
            prefix='download',
            suffix=file_name.suffix,
        )
    )

    # Download by chanks.
    # TODO: timeouts.
    with requests.get(video_file.url, stream=True) as r:
        try:
            r.raise_for_status()
        except requests.HTTPError as ex:
            logger.error('HTTP Error: %s', ex)
            return

        with temp_file_path.open(mode='wb') as f:
            shutil.copyfileobj(r.raw, f)

    # Save into Django storage.
    with temp_file_path.open(mode='rb') as f:
        video_file.original_file.save(
            file_name.name, File(f), save=False
        )
        video_file.save(
            force_update=True,
            update_fields=['original_file']
        )

    temp_file_path.unlink()

    logger.info(
        'File `%s` has been downloaded.',
        file_name.name
    )

    if process:
        logger.info(
            'Run process from download_file %s', video_file_id
        )

        group(
            create_preview.s(video_file.id),
            encode_video_to_mp4.s(video_file.id),
            encode_video_to_webm.s(video_file.id),
        ).delay()

    return video_file_id


@shared_task
def purge_original_files():
    # TODO: Need or not?
    pass

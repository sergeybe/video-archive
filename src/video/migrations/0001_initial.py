# Generated by Django 3.1 on 2020-08-27 20:50

from django.db import migrations, models
import functools
import uuid
import video.models
import video.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_file', models.FileField(blank=True, upload_to='video/original/', validators=[video.validators.validate_video_file_extension], verbose_name='original uploaded file')),
                ('url', models.URLField(blank=True, verbose_name='URL of file for uploading')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, verbose_name='UUID')),
                ('preview', models.ImageField(blank=True, upload_to=functools.partial(video.models.get_adjusted_filename, *(), **{'file_type': 'jpg', 'upload_to': 'images/preview/'}), verbose_name='preview')),
                ('video_as_mp4', models.FileField(blank=True, upload_to=functools.partial(video.models.get_adjusted_filename, *(), **{'file_type': 'mp4', 'upload_to': 'video/mp4/'}), verbose_name='MP4 video file')),
                ('video_as_webm', models.FileField(blank=True, upload_to=functools.partial(video.models.get_adjusted_filename, *(), **{'file_type': 'webm', 'upload_to': 'video/webm/'}), verbose_name='WEBM video file')),
            ],
            options={
                'verbose_name': 'video file',
                'verbose_name_plural': 'video files',
            },
        ),
    ]

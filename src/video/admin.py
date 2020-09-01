from django.contrib import admin

from . import models


@admin.register(models.VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'original_file',
        'created_at',
        'preview',
        'video_as_mp4',
        'video_as_webm',
    )

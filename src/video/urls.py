from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.VideoUploadView.as_view(),
        name='video_upload_page',
    ),
    path(
        'healthcheck/',
        views.health_check,
        name='health_check',
    ),
]

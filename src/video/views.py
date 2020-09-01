from django.db import transaction, connection
from django.http import HttpResponse
from django.views.generic import (
    CreateView
)
from django.urls import reverse_lazy


from .forms import VideoFileForm
from .models import VideoFile
from .tasks import process_video_file


def health_check(request):
    """View for health check."""
    try:
        with connection.cursor() as cursor:
            cursor.execute('select 1')
            one = cursor.fetchone()[0]
            if one != 1:
                raise Exception('The site did not pass the health check')
        return HttpResponse('ok')
    except Exception:  # noqa
        return HttpResponse('error', status=500)


class VideoUploadView(CreateView):
    """Video uploading view."""
    template_name = 'video/video_upload_page.html'

    form_class = VideoFileForm
    success_url = reverse_lazy('video_upload_page')
    queryset = VideoFile.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'video_files': VideoFile.objects.order_by('-id'),
        })
        return context

    @transaction.atomic
    def form_valid(self, form):
        """Process valid form."""

        response = super().form_valid(form)

        transaction.on_commit(
            lambda: process_video_file(form.instance)
        )

        return response

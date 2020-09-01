from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import VideoFile


class VideoFileForm(forms.ModelForm):
    """Form for user file uploading."""

    def clean(self):
        cleaned_data = super().clean()

        original_file = cleaned_data.get('original_file')
        url = cleaned_data.get('url')

        if original_file and url:
            raise ValidationError(
                _('Only one field must be filled.')
            )
        elif not original_file and not url:
            raise ValidationError(
                _('Please enter data in one of these fields.')
            )

    class Meta:
        model = VideoFile

        fields = (
            'original_file',
            'url',
        )

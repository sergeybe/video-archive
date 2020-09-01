from django import template


register = template.Library()


@register.inclusion_tag('video/_video_player.html')
def video_player(video_file):
    """Video player tag."""
    return {
        'video_file': video_file
    }

import logging

from subprocess import Popen, PIPE
from .exceptions import VideoEncodingError, WrongVideoTypeError

# TODO: Create a switchable encoding engine.

logger = logging.getLogger('video.encoding')

cmd_ffmpeg = [
    'ffmpeg',
    '-i',
]

cmd_mp4 = [
    '-vf', 'scale=640:360',
    '-vcodec', 'h264',
    '-acodec', 'aac',
    '-y',
]

cmd_webm = [
    '-vf', 'scale=640:360',
    '-c:v', 'libvpx-vp9',
    '-pix_fmt', 'yuv420p',
    '-y',
]

# cmd_webm = [
#     '-c:v'
#     '-vf', 'scale=640:360',
#     '-vcodec', 'libvpx',
#     '-acodec', 'libvorbis',
#     '-y',
# ]

cmd_jpg = [
    '-frames', '1',
    '-s', '640x360',
    '-ss', '1',
    '-y',
]

codecs = {
    'jpg': cmd_jpg,
    'mp4': cmd_mp4,
    'webm': cmd_webm,
}


def _run_cmd(cmds):

    try:
        return Popen(
            cmds,
            shell=False,
            close_fds=True,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
        )
    except OSError as ex:
        raise VideoEncodingError('Video running error.') from ex


def encode_video_file(src_filname, dst_filename, file_type):

    logger.info(
        'Source file: %s, Destination file: %s, File Type: %s',
        src_filname, dst_filename, file_type
    )

    try:
        cmd = codecs[file_type]
    except IndexError:
        raise WrongVideoTypeError('Wrong video type.')

    process = _run_cmd(
        cmd_ffmpeg + [src_filname] + cmd + [dst_filename],
    )

    # TODO: timeout handling here.
    stdout, stderr = process.communicate()

    returncode = process.returncode

    if returncode != 0:
        logger.error(
            'ffmpeg returncode %d, args: %s, output: %s',
            returncode,
            process.args,
            stderr.decode(),
        )
        raise VideoEncodingError('Video encoding error.')

    return returncode

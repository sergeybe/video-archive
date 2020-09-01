class VideoException(Exception):
    """Base exception for video app."""
    pass


class VideoEncodingError(VideoException):
    """Exception of video encoding."""
    pass


class WrongVideoTypeError(VideoException):
    """Exception for wrong type video."""
    pass

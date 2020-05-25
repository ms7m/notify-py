
# Custom and Clear Exceptions for NotifyPy


class UnsupportedPlatform(Exception):
    """ Unsupported Platform, notify-py might not work as expected """
    pass

class InvalidAudioPath(Exception):
    """ Audio path provided is invalid."""
    pass

class InvalidIconPath(Exception):
    """ Icon Path Provided is Invalid """
    pass

class NotificationFailure(Exception):
    """ Overall function failed """
    pass

class BinaryNotFound(Exception):
    """" A specified binary requirement was not found """
    pass

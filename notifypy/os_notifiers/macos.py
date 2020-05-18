import os
import pathlib
import subprocess
import shlex

from loguru import logger


class MacOSNotifier(object):
    def __init__(self):
        """ Main macOS Notification System, supplied by a custom-made notificator app. 
        Icon Support is **not** supported. You'll need to create your own bundle for that.
        """
        call_find_notificator = self._get_bundled_notificator()
        if call_find_notificator == False:
            logger.info("Unable to find notificator.")
            raise Exception
        if call_find_notificator != False:
            self._notificator_binary = call_find_notificator

    def _get_bundled_notificator(self):
        """ Gets the bundled notificator.app path """
        try:
            current_bundled = os.path.join(
                os.path.dirname(__file__),
                "binaries/Notificator.app/Contents/Resources/Scripts/notificator",
            )
            return current_bundled
        except Exception:
            logger.exception("Unable to get bundled notifier.")
            return False

    def send_notification(
        self, notification_title, notification_subtitle, application_name, **kwargs
    ):
        if kwargs.get("notification_icon"):
            logger.warning(
                "Notification icon is not supported. Read the docs for more information."
            )

        try:

            notification_title = " " if notification_title == "" else notification_title
            notification_subtitle = (
                " " if notification_subtitle == "" else notification_subtitle
            )

            generated_command = [
                self._notificator_binary,
                "--title",
                application_name,
                "--subtitle",
                notification_title,
                "--message",
                notification_subtitle,
            ]

            subprocess.check_output(generated_command)
            return True
        except subprocess.CalledProcessError:
            logger.exception("Unable to send notification.")
            return False
        except Exception:
            logger.exception("Unhandled Exception for sending notifications")
            return False

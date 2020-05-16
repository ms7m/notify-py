
import pathlib
import os
import subprocess
import shlex

from loguru import logger

class WindowsNotifier(object):
    def __init__(self):
        """ Main Windows notification. Supplied by snoretoast.exe """
        call_find_snoretoast = self._get_bundled_snoretoast()
        if call_find_snoretoast == False:
            logger.info("Unable to find snoretoast.exe")
            raise Exception
        if call_find_snoretoast != False:
            self._snoretoast_binary = call_find_snoretoast

    def _get_bundled_snoretoast(self):
        """ Gets the bundled snoretoast.exe path """
        try:
            current_bundled = os.path.join(os.path.dirname(__file__), 'binaries\\snoretoast.exe')
            return current_bundled
        except Exception:
            logger.exception("Unable to get bundled notifier.")
            return False

    def send_notification(self, notification_title, notification_message, notification_icon, notification_application_name="Python Application (Notify.py)"):
        try:
            generated_command = f"{self._snoretoast_binary} -t={notification_title} -m={notification_message} -p={notification_icon} -appId={notification_application_name}"
            formatted_command = shlex.split(generated_command)
            subprocess.check_output(formatted_command)
            return True
        except subprocess.CalledProcessError:
            logger.exception("Unable to send notification.")
            return False
        except Exception:
            logger.exception("Unhandled Exception for Sending Notification.")
            return False
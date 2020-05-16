
from loguru import logger
import subprocess
import shlex


class LinuxNotifier(object):
    def __init__(self):
        """ Main Linux Notification Class 
        
            This uses libnotify's tool of notfiy-send. 
            I'll add support for (and probably use as first choice) sending 
            through dbus.
            
        """
        call_find_notify_send = self._find_installed_notify_send()
        
        if call_find_notify_send == False:
            logger.error("Unable to find notify-send.")
            raise Exception("Unable to find notify-send")        
        if call_find_notify_send != False:
            self._notify_send_binary = call_find_notify_send

    def _find_installed_notify_send(self):
        """ Function to find the path for notify-send """
        try:
            run_which_for_notify_send = subprocess.check_output(
                ["which", "notify-send"]
            )
            return run_which_for_notify_send.decode('utf-8')
        except subprocess.CalledProcessError:
            logger.exception("Unable to find notify-send.")
            return False
        except Exception:
            logger.exception("Unhandled exception for finding notify-send.")
            return False

    def send_notification(self, notification_title, notification_subtitle, notification_icon, **kwargs):
        try:
            generated_command = f'{self._notify_send_binary} "{notification_title}" "{notification_subtitle}"'
            if notification_icon:
                generated_command += f' --icon="{notification_icon}"'

            formatted_command = shlex.split(generated_command)
            subprocess.check_output(formatted_command)
            return True
        except subprocess.CalledProcessError:
            logger.exception("Unable to send notification.")
            return False
        except Exception:
            logger.exception("Unhandled exception for sending notification.")
            return False
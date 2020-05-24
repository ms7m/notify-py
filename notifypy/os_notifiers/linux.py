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

        if not call_find_notify_send:
            logger.error("Unable to find notify-send.")
            raise Exception("Unable to find notify-send")
        if call_find_notify_send:
            self._notify_send_binary = call_find_notify_send

    @staticmethod
    def _find_installed_notify_send():
        """ Function to find the path for notify-send """
        try:
            run_which_for_notify_send = subprocess.check_output(
                ["which", "notify-send"]
            )
            return run_which_for_notify_send.decode("utf-8")
        except subprocess.CalledProcessError:
            logger.exception("Unable to find notify-send.")
            return False
        except Exception:
            logger.exception("Unhandled exception for finding notify-send.")
            return False

    def send_notification(
        self,
        notification_title,
        notification_subtitle,
        notification_icon,
        notification_audio,
        **kwargs,
    ):
        try:

            notification_title = " " if notification_title == "" else notification_title
            notification_subtitle = (
                " " if notification_subtitle == "" else notification_subtitle
            )

            generated_command = [
                self._notify_send_binary.strip(),
                notification_title,
                notification_subtitle,
            ]

            if notification_icon:
                generated_command.append(f"--icon={shlex.quote(notification_icon)}")

            if notification_audio:
                subprocess.Popen(
                    ["aplay", notification_audio],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                )

            subprocess.check_output(generated_command)
            return True
        except subprocess.CalledProcessError:
            logger.exception("Unable to send notification.")
            return False
        except Exception:
            logger.exception("Unhandled exception for sending notification.")
            return False

import platform
import os
import pathlib
import threading


from loguru import logger


from .os_notifiers import LinuxNotifier, MacOSNotifier, WindowsNotifier


class Notify:
    def __init__(
        self,
        default_notification_title="Default Title",
        default_notification_message="Default Message",
        default_notification_application_name="Python Application (notify.py)",
        default_notification_icon=os.path.join(
            os.path.dirname(__file__), "py-logo.png"
        ),
    ):
        """ Main Notify Object, this handles communcation with other functions to send notifications across different platforms """
        self._notifier_detect = self._selected_notification_system()
        self._notifier = self._notifier_detect()

        # Set the defaults.

        self._notification_title = default_notification_title
        self._notification_message = default_notification_message
        self._notification_application_name = default_notification_application_name
        self._notification_icon = default_notification_icon

    def _selected_notification_system(self):
        selected_platform = platform.system()
        if selected_platform == "Linux":
            return LinuxNotifier
        elif selected_platform == "Darwin":
            return MacOSNotifier
        elif selected_platform == "Windows":
            return WindowsNotifier
        else:
            raise Exception("Unable to detect platform.")

    @property
    def icon(self):
        return self._notification_icon

    @icon.setter
    def icon(self, new_icon_path):
        # first detect if it already exists.
        if pathlib.Path(new_icon_path).exists() == True:
            self._notification_icon = str(pathlib.Path(new_icon_path).absolute())
        else:
            # Ok doesn't exist, let's try a join
            if (
                pathlib.Path(
                    os.path.join(os.path.dirname(__file__), new_icon_path)
                ).exists()
                == True
            ):
                self._notification_icon = os.path.join(
                    os.path.dirname(__file__), new_icon_path
                )
            else:
                raise Exception("Unable to set icon.")

    @property
    def title(self):
        return self._notification_title

    @title.setter
    def title(self, new_title):
        self._notification_title = new_title

    @property
    def message(self):
        return self._notification_message

    @message.setter
    def message(self, new_message):
        self._notification_message = new_message

    @property
    def application_name(self):
        return self._notification_application_name

    @application_name.setter
    def application_name(self, new_application_name):
        self._notification_application_name = new_application_name

    def send(self, block=True):
        # if block is True, wait for the notification to complete and return if it was successful
        # else start the thread and return a threading.Event that will determine when the notification was successful
        event = threading.Event()
        try:
            thread = threading.Thread(
                target=lambda: self.start_notification_thread(event)
            )
            thread.name = "notify.py"
            thread.start()
            if block:
                thread.join(timeout=35)
                return event.is_set()
            return event
        except Exception:
            logger.exception("Exception in running send-Notification.")
            raise

    def start_notification_thread(self, event):
        result = self.send_notification(
            supplied_title=self._notification_title,
            supplied_message=self._notification_message,
            supplied_application_name=self._notification_application_name,
            supplied_icon_path=self._notification_icon,
        )
        if result:
            event.set()
        else:
            event.clear()

    def send_notification(
        self,
        supplied_title,
        supplied_message,
        supplied_application_name,
        supplied_icon_path,
    ):
        try:
            attempt_to_send_notifiation = self._notifier.send_notification(
                notification_title=supplied_title,
                notification_subtitle=supplied_message,
                application_name=supplied_application_name,
                notification_icon=supplied_icon_path,
            )
            if attempt_to_send_notifiation == True:
                logger.info("Sent notification.")
            else:
                logger.info("unable to send notification.")

            return attempt_to_send_notifiation
        except Exception:
            logger.exception("Exception on sending notification.")
            raise

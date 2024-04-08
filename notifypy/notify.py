import platform
import os
import pathlib
import threading


from loguru import logger
from .exceptions import (
    UnsupportedPlatform,
    InvalidAudioPath,
    InvalidIconPath,
    NotificationFailure,
    BinaryNotFound,
    InvalidAudioFormat,
)

from .os_notifiers._base import BaseNotifier


class Notify:
    def __init__(
        self,
        title="",
        message="",
        app_name="Python",
        urgency='normal',
        icon=None,
        audio=None,
        enable_logging=False,
        **kwargs,
    ):
        """Main Notify Class.

        Optional Arugments:
            override_detected_notification_system: Optional Kwarg that allows for the use of overrding the detected notifier.
            disable_logging: Optional Kwarg that will disable stdout logging from this library.
            custom_mac_notificator: Optional Kwarg for a custom mac notifier. (Probably because you want to change the icon.). This is a direct path to the parent directory (.app).

        """

        if not enable_logging:
            check_if_enable_logging_env = os.getenv("notifypyEnableLogging")
            if check_if_enable_logging_env:
                logger.warning(
                    f"System environment variable for enabling logging is active. Ignoring parameter passed. ({enable_logging})"
                )
            else:
                logger.disable("notifypy")
        else:
            logger.info("Logging is enabled.")

        if kwargs.get("use_custom_notifier"):
            """
            This optional kwarg allows for the use of overriding the detected notifier.
            Use at your own risk
            """
            selected_override = kwargs.get("use_custom_notifier")
            if issubclass(selected_override, BaseNotifier):
                self._notifier_detect = selected_override
            else:
                raise ValueError("Overrided Notifier must inherit from BaseNotifier.")
        else:
            check_if_user_override_detection = kwargs.get(
                "override_detected_notification_system"
            )
            if check_if_user_override_detection:
                self._notifier_detect = self._selected_notification_system(**kwargs)
            else:
                self._notifier_detect = self._selected_notification_system()

        # Initialize.
        self._notifier = self._notifier_detect(**kwargs)

        # Set the defaults.
        self._notification_title = title
        self._notification_message = message
        self._notification_application_name = app_name
        self._notification_urgency = urgency

        # These defaults require verification
        if icon:
            self._notification_icon = self._verify_icon_path(icon)
        else:
            self._notification_icon = str(
                os.path.join(os.path.dirname(__file__), "py-logo.png")
            )

        if audio:
            self._notification_audio = self._verify_audio_path(
                audio
            )
        else:
            self._notification_audio = None

    @staticmethod
    def _selected_notification_system(
        override_detection: str = False,
        override_windows_version_detection: bool = False,
        linux_use_legacy_notifier: bool = False,
    ):

        if override_detection:
            logger.info(f"chosen to override to {override_detection}.")
            selected_platform = override_detection
        else:
            selected_platform = platform.system()

        if selected_platform == "Darwin":
            from .os_notifiers.macos import MacOSNotifier

            return MacOSNotifier
        elif selected_platform == "Windows":
            if platform.release() == "10":
                from .os_notifiers.windows import WindowsNotifier

                return WindowsNotifier

            if override_windows_version_detection == True:
                from .os_notifiers.windows import WindowsNotifier

                return WindowsNotifier

            raise UnsupportedPlatform(
                f"This version of Windows ({platform.release()}) is not supported."
            )
        else:
            if selected_platform != "Linux":
                logger.warning(f'{selected_platform} might not be supported!')

            if linux_use_legacy_notifier:
                from .os_notifiers.linux import LinuxNotifierLibNotify

                return LinuxNotifierLibNotify
            else:

                from .os_notifiers.linux import NOTIFY

                if NOTIFY:
                    from .os_notifiers.linux import LinuxNotifierLibNotify

                    return LinuxNotifierLibNotify
                else:
                    from .os_notifiers.linux import LinuxNotifier

                    return LinuxNotifier

    @staticmethod
    def _verify_audio_path(new_audio_path):
        # we currently only support .wav files
        if not new_audio_path.endswith(".wav"):
            raise InvalidAudioFormat

        # first detect if it already exists.
        if pathlib.Path(new_audio_path).exists():
            return str(pathlib.Path(new_audio_path).absolute())
        else:
            # Ok doesn't exist, let's try a join
            if pathlib.Path(
                os.path.join(os.path.dirname(__file__), new_audio_path)
            ).exists():
                return str(os.path.join(os.path.dirname(__file__), new_audio_path))
            else:
                raise InvalidAudioPath(
                    f"Could not find specified audio path to '{new_audio_path}'. Please check if it exists."
                )

    @staticmethod
    def _verify_icon_path(new_icon_path):
        # first detect if it already exists.
        if pathlib.Path(new_icon_path).exists():
            return str(pathlib.Path(new_icon_path).absolute())
        else:
            # Ok doesn't exist, let's try a join
            if pathlib.Path(
                os.path.join(os.path.dirname(__file__), new_icon_path)
            ).exists():
                return os.path.join(os.path.dirname(__file__), new_icon_path)
            else:
                raise InvalidIconPath(
                    f"Could not find specified icon path to '{new_icon_path}'. Please check if it exists."
                )

    @property
    def audio(self):
        """A direct path to a '.wav' audio file.

        Returns:
            str: direct path to '.wav' audio file.
        """
        return self._notification_audio

    @audio.setter
    def audio(self, new_audio_path):
        self._notification_audio = self._verify_audio_path(new_audio_path)

    @property
    def icon(self):
        """A direct path to a '.png' image file.
        Note: .jpg might work, but hasn't been fully tested.
        macOS does not support setting this attribute.

        Returns:
            str: A direct path to a '.png' image file.
        """
        return self._notification_icon

    @icon.setter
    def icon(self, new_icon_path):
        self._notification_icon = self._verify_icon_path(new_icon_path)

    @property
    def title(self):
        """The top (often bolded) message for the notification.

        macOS (as of 0.2.0) the application name takes the bolded area, while the title is directly below it.

        Returns:
            str: The top (often bolded) message for the notification.
        """
        return self._notification_title

    @title.setter
    def title(self, new_title):
        self._notification_title = new_title

    @property
    def message(self):
        """The main message to be displayed in the notification. Directly below the title.

        Returns:
            str: The message for the notification.
        """
        return self._notification_message

    @message.setter
    def message(self, new_message):
        self._notification_message = new_message

    @property
    def app_name(self):
        """The application name that will be displayed (if the platform allows it.)
        Windows and macOS requires an application name to be displayed.

        Returns:
            str: the application name
        """
        return self._notification_application_name

    @app_name.setter
    def app_name(self, new_application_name):
        self._notification_application_name = new_application_name

    @property
    def urgency(self):
        """The urgency of the notification (low, normal, critical) 
        Works only with libnotify (Linux), as of now

        Returns:
            str: The urgency of the notification.
        """
        return self._notification_urgency

    @urgency.setter
    def urgency(self, new_urgency):
        self._notification_urgency = new_urgency

    def send(self, block=True):
        """Main send function. This will take all attributes sent and forward to
        send_notification.

        Args:
            block (bool, optional): Optional value to not to block the main application thread. If enabled this won't return a bool. Defaults to True.

        Returns:
            bool: as long as the block isn't set to False.
        """
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
            logger.exception("Unhandled exception for sending notification.")
            raise

    def start_notification_thread(self, event):
        """Function for sending notification via a seperate thread.
        You don't need to call this directly. Do .send(block=False)

        Args:
            event (threading.Thread): event to be recieved.
        """
        result = self.send_notification(
            supplied_title=self._notification_title,
            supplied_message=self._notification_message,
            supplied_application_name=self._notification_application_name,
            supplied_urgency=self._notification_urgency,
            supplied_icon_path=self._notification_icon,
            supplied_audio_path=self._notification_audio,
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
        supplied_urgency,
        supplied_icon_path,
        supplied_audio_path,
    ):
        """A function to handles sending all required variables to respected OS-Notifier.

        Args:
            supplied_title str: Title for notification
            supplied_message str: Message for notification
            supplied_application_name str: Application name for notification (if platform needs it)
            supplied_urgency str: low, normal, critical | Notification urgency
            supplied_icon_path str: Direct path to custom icon
            supplied_audio_path str: Direct path to custom audio

        Raises:
            NotificationFailure: If there was an Exception in sending the notification.

        Returns:
            bool: True if the notification was sent.
        """
        try:
            attempt_to_send_notifiation = self._notifier.send_notification(
                notification_title=str(supplied_title),
                notification_subtitle=str(supplied_message),
                application_name=str(supplied_application_name),
                notification_urgency=str(supplied_urgency),
                notification_icon=str(supplied_icon_path),
                notification_audio=str(supplied_audio_path)
                if supplied_audio_path
                else None,
            )
            if attempt_to_send_notifiation:
                logger.info("Sent notification.")
            else:
                logger.info("unable to send notification.")

            return attempt_to_send_notifiation
        except Exception:
            logger.exception("Exception on sending notification.")
            raise NotificationFailure

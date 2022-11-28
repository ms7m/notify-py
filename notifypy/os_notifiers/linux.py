from loguru import logger
import subprocess
import shlex

from ..exceptions import BinaryNotFound
from ._base import BaseNotifier

try:
    from jeepney import DBusAddress, new_method_call
    from jeepney.io.blocking import open_dbus_connection
    from shutil import which

    NOTIFY = which('notify-send') # alternatively: from ctypes.util import find_library 

    if NOTIFY:
        logger.info("libnotify found, using it for notifications")
    else: # check if dbus is available
        import os
        _dbus_address = os.getenv("DBUS_SESSION_BUS_ADDRESS")
        if _dbus_address:
            logger.info("Jeepney and Dbus is available. Using DBUS for notifications..")
        else:
            raise ImportError

    APLAY = which('aplay')

    if APLAY == None:
        logger.debug("aplay binary not installed.. audio will not work!")


except ImportError:
    logger.error("libnotify nor DBUS installed.")


class LinuxNotifierLibNotify(BaseNotifier):
    def __init__(self, **kwargs):
        """Main Linux Notification Class

        This uses libnotify's tool of notfiy-send.
        """
        pass

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
                NOTIFY,
                notification_title,
                notification_subtitle,
            ]

            if notification_icon:
                generated_command.append(f"--icon={shlex.quote(notification_icon)}")

            if kwargs.get("application_name"):
                generated_command.append(
                    f"--app-name={shlex.quote(kwargs.get('application_name'))}"
                )

            if kwargs.get('notification_urgency'):
                generated_command.extend(["-u", kwargs.get('notification_urgency')])

            logger.debug(f"Generated command: {generated_command}")
            if notification_audio:

                if APLAY == None:
                    raise BinaryNotFound("aplay (Alsa)")

                subprocess.Popen(
                    [APLAY, notification_audio],
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


class LinuxNotifier(BaseNotifier):
    def __init__(self, **kwargs):
        """Main Linux Notification Class (Dbus)

        This uses jeepney library as the dbus communicator

        """

        self._dbus_notifications = DBusAddress(
            "/org/freedesktop/Notifications",
            bus_name="org.freedesktop.Notifications",
            interface="org.freedesktop.Notifications",
        )


    def send_notification(
        self,
        notification_title,
        notification_subtitle,
        notification_icon,
        notification_audio,
        **kwargs,
    ):
        try:
            _attempt_to_open_dbus_connection = open_dbus_connection(bus="SESSION")
            logger.debug("linux: opened dbus connection")
        except Exception:
            logger.exception("issue with opening DBUS connection!")
            return False

        try:
            notification_title = " " if notification_title == "" else notification_title
            notification_subtitle = (
                " " if notification_subtitle == "" else notification_subtitle
            )

            if notification_audio:
                # TODO: https://specifications.freedesktop.org/notification-spec/latest/ar01s09.html
                # use sound param instead of relying on alsa?

                if APLAY == None:
                    raise BinaryNotFound("aplay (Alsa)")

                subprocess.Popen(
                    [APLAY, notification_audio],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                )
            create_notification = new_method_call(
                self._dbus_notifications,
                "Notify",
                "susssasa{sv}i",
                (
                    kwargs.get("application_name"),  # App name
                    0,  # Not replacing any previous notification
                    notification_icon if notification_icon else "",  # Icon
                    notification_title,  # Summary
                    notification_subtitle,
                    [],
                    {},  # Actions, hints
                    -1,  # expire_timeout (-1 = default)
                ),
            )
            reply = _attempt_to_open_dbus_connection.send_and_get_reply(
                create_notification, timeout=2
            )
            logger.debug(f"confirmed notification sent! id: {reply}")
            _attempt_to_open_dbus_connection.close()
            return True

        except Exception:
            logger.exception("issue with sending through dbus!")
            return False

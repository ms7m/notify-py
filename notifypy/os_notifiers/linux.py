from loguru import logger
import subprocess
import shlex

from ..exceptions import BinaryNotFound, NotificationFailure, LinuxDbusException
from ._base import BaseNotifier

try:
    from jeepney import DBusAddress, new_method_call
    from jeepney.io.blocking import open_dbus_connection
    import os

    # check if dbus is available
    _dbus_address = os.getenv("DBUS_SESSION_BUS_ADDRESS")
    if _dbus_address:
        logger.info("Jeepney and Dbus is available. Using DBUS for notifications..")
        USE_LEGACY = False
    else:
        logger.error(
            "Jeepney is available but DBUS is not. Using legacy notification instead."
        )
        USE_LEGACY = True
except ImportError:
    logger.error("DBUS suppport not installed. Using libnotify for notifications!")
    USE_LEGACY = True


class LinuxNotifierLibNotify(BaseNotifier):
    def __init__(self):
        """Main Linux Notification Class

        This uses libnotify's tool of notfiy-send.
        I'll add support for (and probably use as first choice) sending
        through dbus.

        """

        call_find_notify_send = self._find_installed_notify_send()

        if not call_find_notify_send:
            logger.error("Unable to find notify-send.")
            raise BinaryNotFound("notify-send")
        if call_find_notify_send:
            self._notify_send_binary = call_find_notify_send

        call_find_aplay = self._find_installed_aplay()
        if not call_find_aplay:
            # no Aplay is available.
            self._aplay_binary = False
        else:
            self._aplay_binary = call_find_aplay

    @staticmethod
    def _find_installed_aplay():
        """Function to find the path for notify-send"""
        try:
            run_which_for_aplay = subprocess.check_output(["which", "aplay"])
            return run_which_for_aplay.decode("utf-8")
        except subprocess.CalledProcessError:
            logger.exception("Unable to find aplay.")
            return False
        except Exception:
            logger.exception("Unhandled exception for finding aplay.")
            return False

    @staticmethod
    def _find_installed_notify_send():
        """Function to find the path for notify-send"""
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

            if kwargs.get("application_name"):
                generated_command.append(
                    f"--app-name={shlex.quote(kwargs.get('application_name'))}"
                )

            logger.debug(f"Generated command: {generated_command}")
            if notification_audio:

                if self._aplay_binary == False:
                    raise BinaryNotFound("aplay (Alsa)")

                subprocess.Popen(
                    [self._aplay_binary.strip(), notification_audio],
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

        call_find_aplay = self._find_installed_aplay()
        if not call_find_aplay:
            # no Aplay is available.
            self._aplay_binary = False
            logger.debug("aplay binary not installed.. audio will not work!")
        else:
            self._aplay_binary = call_find_aplay

        if kwargs.get("linux_fallback_libnotify"):
            self._fallback_to_libnotify = True
        else:
            self._fallback_to_libnotify = False

    @staticmethod
    def _find_installed_aplay():
        """Function to find the path for notify-send"""
        try:
            run_which_for_aplay = subprocess.check_output(["which", "aplay"])
            return run_which_for_aplay.decode("utf-8")
        except subprocess.CalledProcessError:
            logger.exception("Unable to find aplay.")
            return False
        except Exception:
            logger.exception("Unhandled exception for finding aplay.")
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
            _attempt_to_open_dbus_connection = open_dbus_connection(bus="SESSION")
            logger.debug("linux: opened dbus connection")
        except Exception:
            logger.exception("issue with opening DBUS connection!")
            if self._fallback_to_libnotify == True:
                logger.debug("falling back to libnotify!")
                return LinuxNotifierLibNotify().send_notification(
                    notification_title,
                    notification_subtitle,
                    notification_icon,
                    notification_audio,
                    **kwargs,
                )
            else:
                logger.exception(
                    "there was an exception trying to open the dbus connection. fallback was not enabled, therefore this will return False."
                )
                return False

        try:
            notification_title = " " if notification_title == "" else notification_title
            notification_subtitle = (
                " " if notification_subtitle == "" else notification_subtitle
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
            if self._fallback_to_libnotify == True:
                logger.debug("falling back to libnotify!")
                return LinuxNotifierLibNotify().send_notification(
                    notification_title,
                    notification_subtitle,
                    notification_icon,
                    notification_audio,
                    **kwargs,
                )
            return False

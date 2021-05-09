import pathlib
import os
import subprocess
from xml.etree import ElementTree
import tempfile
import uuid
import codecs

from loguru import logger
from ._base import BaseNotifier


class WindowsNotifier(BaseNotifier):
    def __init__(self):
        """Main Notification System for Windows. Basically ported from go-toast/toast"""

        # Create the base
        self._top_ps1_script = f"""
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
"""

    def _generate_notification_xml(
        self,
        application_id,
        notification_title,
        notification_subtitle,
        notification_icon,
        notification_audio,
    ):

        # Create the top <toast> element
        top_element = ElementTree.Element("toast")
        # set the duration for the top element
        top_element.set("duration", "short")

        # create the <visual> element
        visual_element = ElementTree.SubElement(top_element, "visual")

        # create <binding> element
        binding_element = ElementTree.SubElement(visual_element, "binding")
        # add the required attribute for this.
        # For some reason, go-toast set the template attribute to "ToastGeneric"
        # but it never worked for me.
        binding_element.set("template", "ToastImageAndText02")

        # create <image> element
        image_element = ElementTree.SubElement(binding_element, "image")
        # add an Id
        image_element.set("id", "1")
        # add the src
        image_element.set("src", notification_icon)

        # add the message and title

        title_element = ElementTree.SubElement(binding_element, "text")
        title_element.set("id", "1")
        title_element.text = notification_title

        message_element = ElementTree.SubElement(binding_element, "text")
        message_element.set("id", "2")
        message_element.text = notification_subtitle

        if notification_audio:
            # the user has provided his own audio file, no need to play the default sound.
            audio_element = ElementTree.SubElement(top_element, "audio")
            audio_element.set("silent", "true")

        # Great we have a generated XML notification.
        # We need to create the rest of the .ps1 file and dump it to the temporary directory

        generated_ps1_file = f"""
{self._top_ps1_script}
$APP_ID = "{application_id}"

$template = @"
{ElementTree.tostring(top_element, encoding="utf-8").decode('utf-8')}
"@

$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = New-Object Windows.UI.Notifications.ToastNotification $xml
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($APP_ID).Show($toast)
"""
        return generated_ps1_file

    def send_notification(
        self,
        notification_title,
        notification_subtitle,
        notification_icon,
        application_name,
        notification_audio,
    ):
        generated_file = self._generate_notification_xml(
            notification_title=notification_title,
            notification_subtitle=notification_subtitle,
            notification_icon=notification_icon,
            application_id=application_name,
            notification_audio=notification_audio,
        )

        if notification_audio:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(
                [
                    "Powershell",
                    f'(New-Object Media.SoundPlayer "{notification_audio}").playsync()',
                ],
                startupinfo=startupinfo,
            )

        # open the temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            generated_uuid_file = str(uuid.uuid4())
            with codecs.open(
                f"{temp_dir}/{generated_uuid_file}.ps1", "w", "utf_8_sig"
            ) as ps1_file:
                ps1_file.write(generated_file)
            # exceute the file
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(
                [
                    "Powershell",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    f"{generated_uuid_file}.ps1",
                ],
                cwd=temp_dir,
                startupinfo=startupinfo,
            ).wait()
        return True

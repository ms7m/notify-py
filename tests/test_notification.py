import notifypy
import pytest
import pathlib
import platform


from notifypy import BaseNotifier


def test_normal_notification():
    n = notifypy.Notify()
    assert n.send() == True


def test_multiline_notification():
    n = notifypy.Notify()
    n.message = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore magna 
aliqua. Ut enim ad minim veniam, quis nostrud exercitation 
ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit 
esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""
    assert n.send() == True


def test_notification_with_emoji():
    n = notifypy.Notify()
    n.title = "🐐"
    n.message = "also known as Kanye West"


def test_notification_with_double_quotes():
    n = notifypy.Notify()
    n.title = '" Yes "Yes"'
    assert n.send() == True


def test_notification_with_special_chars():
    n = notifypy.Notify()
    n.message = '"""""; """ ;;# ##>>> <<>>< </>'
    assert n.send() == True


def test_blank_message_notification():
    n = notifypy.Notify()
    n.message = ""
    assert n.send() == True


def test_blank_title_notification():
    n = notifypy.Notify()
    n.title = ""
    assert n.send() == True


def test_rtl_language_notification():
    n = notifypy.Notify()
    n.title = "مرحبا كيف الحال؟"
    assert n.send() == True


def test_blocking_notification():
    n = notifypy.Notify()
    assert n.send(block=True) == True


def test_non_blocking_notification():
    n = notifypy.Notify()
    thread_notify = n.send(block=False)
    assert thread_notify.wait()


def test_custom_audio():
    n = notifypy.Notify()
    n.audio = "notifypy/example_notification_sound.wav"
    assert n.send() == True


def test_custom_audio_no_file():
    n = notifypy.Notify()
    with pytest.raises(notifypy.exceptions.InvalidAudioFormat):
        n.audio = "not a file!"


def test_non_existant_icon():
    n = notifypy.Notify()
    with pytest.raises(notifypy.exceptions.InvalidIconPath):
        n.icon = "ttt"


def test_invalid_icon_default():
    with pytest.raises(notifypy.exceptions.InvalidIconPath):
        n = notifypy.Notify(default_notification_icon="sadfiasjdfisaodfj")


def test_invalid_audio_default():
    with pytest.raises(notifypy.exceptions.InvalidAudioPath):
        n = notifypy.Notify(default_notification_audio="dsaiofj/sadf/vv.wav")


def test_invalid_audio_format_default():
    with pytest.raises(notifypy.exceptions.InvalidAudioFormat):
        n = notifypy.Notify(default_notification_audio="asdfiojasdfioj")


def test_custom_notification():
    class CustomNotificator(BaseNotifier):
        def __init__(self, **kwargs):
            pass

    n = notifypy.Notify(override_detected_notification_system=CustomNotificator)
    assert n._notifier_detect == CustomNotificator


def test_invalid_custom_notification():
    class CustomNotificator:
        pass

    with pytest.raises(ValueError):
        notifypy.Notify(override_detected_notification_system=CustomNotificator)


def test_unexposed_inherit_baseNotifier():
    with pytest.raises(NotImplementedError):

        class CustomNotificator(BaseNotifier):
            pass

        CustomNotificator().send_notification()


@pytest.mark.skipif(platform.system() != "Darwin", reason="macOS only test.")
def test_macOS_custom_notificator():
    custom_notificator_path = str(
        pathlib.Path(__file__).resolve().parent / "Notificator.app"
    )
    n = notifypy.Notify(custom_mac_notificator=custom_notificator_path)
    assert (
        n._notifier._notificator_binary
        == custom_notificator_path + "/Contents/Resources/Scripts/notificator"
    )
    assert n.send() == True

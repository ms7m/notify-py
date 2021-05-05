from .notify import Notify
import argparse


def _enable_argument_parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(
        description="Send cross-platform desktop notifications."
    )

    # Required Arguments.
    argument_parser.add_argument(
        "--title",
        "-t",
        dest="userCreatedTitle",
        help="Notification Title",
        required=True,
    )
    argument_parser.add_argument(
        "--message",
        "-m",
        dest="userCreatedMessage",
        help="Notification Message",
        required=True,
    )
    argument_parser.add_argument(
        "--applicationName",
        "-a",
        dest="userCreatedApplicationName",
        help="Notification application name",
        required=True,
    )
    # Optional Arguments
    argument_parser.add_argument(
        "--iconPath",
        "-i",
        dest="userCreatedIconPath",
        help="Notification Icon. (Not available on macOS). Specify a direct path to icon.",
        required=False,
    )
    argument_parser.add_argument(
        "--soundPath",
        "-s",
        dest="userCreatedSoundPath",
        help="Notification Sound. Specify a direct path.",
        required=False,
    )

    # Extras
    argument_parser.add_argument(
        "--enableLogging", dest="userCreatedEnableLogging", action="store_true"
    )
    argument_parser.add_argument(
        "--overridePlatform",
        dest="userCreatedOverridePlatform",
        help="Overrides the check for determining appropriate notifier. (Windows, Darwin, Linux).",
        required=False,
    )

    return argument_parser


def entry():
    """Entrypoint for CLI (Notify-py)"""
    parser = _enable_argument_parser()
    arguments_recieved = parser.parse_args()

    _current_extra_built_kwargs = {}

    if arguments_recieved.userCreatedOverridePlatform in ["Windows", "Darwin", "Linux"]:
        _current_extra_built_kwargs[
            "use_custom_notifier"
        ] = arguments_recieved.userCreatedOverridePlatform

    if arguments_recieved.userCreatedEnableLogging == True:
        _current_extra_built_kwargs["enable_logging"] = True

    if arguments_recieved.userCreatedSoundPath:
        _current_extra_built_kwargs[
            "default_notification_audio"
        ] = arguments_recieved.userCreatedSoundPath

    if arguments_recieved.userCreatedIconPath:
        _current_extra_built_kwargs[
            "default_notification_icon"
        ] = arguments_recieved.userCreatedIconPath
    Notify(
        default_notification_title=arguments_recieved.userCreatedTitle,
        default_notification_message=arguments_recieved.userCreatedMessage,
        default_notification_application_name=arguments_recieved.userCreatedApplicationName,
        **_current_extra_built_kwargs
    ).send()

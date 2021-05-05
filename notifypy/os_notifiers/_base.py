class BaseNotifier(object):
    """This is a base object to be inheritied by each notifier. You can inherit this if you choose to create your own notifier."""

    def send_notification(self, **kwargs):
        raise NotImplementedError(
            "You'll need to expose a send_notification method in your notifier."
        )

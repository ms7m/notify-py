# Custom Notifications

Custom notifications can be made if you choose.

```python
from notifypy import BaseNotifier
from notifypy import Notify


class CustomNotifier(BaseNotifier):
    def __init__(self, **kwargs):
        pass

    def send_notification(self, **kwargs):
        print("Yes. This works.")
        return True


n = Notify(
    override_detected_notification_system=CustomNotifier,
    # This can be anything for the key.
    custom_notification_arguments="Bob",
)

n.send()
```



They must

- Inherit ``BaseNotifier``
- Expose ``send_notification``.

If you wish to have custom arguments, you can do add ``kwargs`` and notify.py will forward them.
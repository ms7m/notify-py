



# Sending Notifications.



## ⚠️ Important Caveats

As it stands (May 18, 2020), this is simply a notification service. There is **no** support for embedding custom actions (buttons, dialogs) regardless of platform. Other then telling you if the shell command was sent, there is also no confirmation on user action on the notification. 



macOS does ***\*not\**** support custom icons on the fly.. You will need to bundle a customized version of the notifier embedded with your custom icon. 

***



## Sending Notifications with a Custom Icon

> Caution: **macOS** does not support custom icons on the fly. You'll need to generate customized binary and point notify-py to it. 



```python
from notifypy import Notify

notification = Notify()
notification.title = "Cool Title"
notification.message = "Even cooler message."
notification.icon = "path/to/icon.png"

notification.send()

```

.pngs were tested on all platforms. Windows might require a smaller version of your .png. 



***

## Sending Notifications with a Custom Sound

> Caution: Be wary, this will be play a sound fully. Please be responsible.

```python
from notifypy import Notify

notification = Notify()
notification.title = "Cool Title"
notification.message = "Even cooler message."
notification.audio = "path/to/audio/file.wav"

notification.send()

```



***

## Sending Notifications without blocking.

By default, execution of your script might stop when sending the notifications. While it's not crazy limited (often >1sec). You might want to make sure that all notification sending happens outside the scope of the app. 

```python
from notifypy import Notify

notification = Notify()
notification.send(block=False)

```

This spawns a separate thread for creating and sending the notification.

***

## Sending with a Default Notification Title/Message/Icon/Sound

```python

from notifypy import Notify

notification = Notify(
  default_notification_title="Function Message",
  default_application_name="Great Application",
  default_notification_icon="path/to/icon.png",
  default_notification_audio="path/to/sound.wav"
)

def your_function():
  # stuff happening here.
  notification.message = "Function Result"
  notification.send()
```



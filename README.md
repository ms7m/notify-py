<div align="center">
<br>
  <h1> notify.py </h1>
  <i> Cross platform desktop notifications for Python scripts and applications.</i>
</div>

![Test Linux](https://github.com/ms7m/notify-py/workflows/Test%20Linux/badge.svg)
 ![Test macOS](https://github.com/ms7m/notify-py/workflows/Test%20macOS/badge.svg)
 ![Test Windows](https://github.com/ms7m/notify-py/workflows/Test%20Windows/badge.svg)

## How are they sent?

- Windows
  - Notifications are natively sent with ``windows.ui.notifications`` through Powershell.
- macOS
  - Notifications are sent with a bundled .app. 
    - Please read below on setting application icons.
- Linux
  - Notifications are sent with notify-send.



No dependencies are required other than loguru.

***



## Install

- PyPi
  - ``pip install "notify-py"``
- Install the latest development build
  - Install the wheel from Github Releases Tab.





***

## Usage



```python
# Send a simple text notification.

import notifypy

notification = notifypy.Notify()
notification.send()

# This sends a notification with the default values.


# Updating the values

notification.title = "Really Cool Title"
notification.message = "Even cooler message."
notification.icon = "path/to/icon.png"
notification.application_name = "SuperCoolApp"

notification.send()


```

```python
import notifypy

# You can quickly initalize with a 'default' message.

notifification = notifypy.Notify(
	default_notification_title="Function completed",
    defualt_application_name="SuperLongFunction"
)

def super_long_function():
    # super long stuff here
    result = result_of_long_function
    
   	notification.message = str(result_of_long_function)
    notification.send()
    
```

```python

import notifypy

notification = notify.Notify()
# Send the notification without blocking.

notification.send(block=False)
```
***



## Important Caveats 

- As it stands (May 18, 2020), this is simply a notification service. There is *no* support for embedding custom actions (buttons, dialogs) regardless of platform. Other then telling you if the shell command was sent, there is also no confirmation on user action on the notification. 

~~- This is **blocking**. This will block most programs when *sending* the notification. This will be changed in the future. This *may* cause GUI applications to freeze. Do your own testing.~~ v0.0.8.

- There is no support for sending custom sounds, and is silent for most platforms. (notable exclusion is windows.). This will be changed in the future.
- macOS does **not** support custom icons OTF. You will need to bundle a customized version of the notifier embedded with your custom icon. 



### Windows Specific.

- No support for balloon tips (pre Win10).. This will be changed in the future.

***

### Special Thanks

- https://github.com/go-toast/toast - Ported their Windows 10 toast notification to Python.

- [Vítor Galvão](https://github.com/vitorgalvao) for https://github.com/vitorgalvao/notificator

# Custom Icons for macOS		

Due to restrictions set by macOS, there isn't a way to add a custom icon on the fly. You'll need to create a customized version of the notifier used. 

***

**Clone the notificator repo**

```
git clone https://github.com/vitorgalvao/notificator
```

Follow the instructions in the README.md for adding a custom icon. It will spit out an ``.app``.  You'll need it for later.

***

You now have two options. 

- You can either build a custom wheel from this repository. This will include your custom notificator.
- You can provide a path to the custom notificator, and tell notify.py to use that one instead of the bundled version.

***



## Option 1

**Clone the notify.py repo.**

```
git clone https://github.com/ms7m/notify-py
```


**Create your virtual environment**

```
python -m venv venv
```

**Install the dependencies to build**

```
python3 -m pip install loguru
python3 -m pip install --user --upgrade setuptools wheel
```

After that's done, copy the .app into ``notifypy/os_notifiers/binary`` folder. 

Make sure the executable inside ``/os_notifiers/binary/Notificator.app/Contents/Resources/Scripts/notificator``has the needed permissions to execute. 

**Test before building**

```python
import notifypy
n = notifypy.Notify()
n.send()
```

You can also run the tests inside the ``tests/`` folder. (Install pytest before)

**If everything works out, go ahead and build the wheel.**

```
python3 setup.py sdist bdist_wheel
```

You'll be supplied with a .whl inside the ``dist/`` folder. 

*How you distribute this wheel is up to you.  It's probably best to add it to a git repo, and add it to your requirements.txt file.*

***



## Option 2

If you prefer, you can also forward a path to your custom notificator to notify.py by using the optional kwarg ``custom_mac_notificator``.

```python
import notifypy

n = notifypy.Notify(
	custom_mac_notificator="path/to/custom.app"
)
```

Make sure that the notificator is executable. 
# Documentation for Notify.py

<div align="center">
  <p align="center">
    <img src="https://github.com/ms7m/notify-py/workflows/Test%20Linux/badge.svg">
    <img src="https://github.com/ms7m/notify-py/workflows/Test%20macOS/badge.svg">
    <img src="https://github.com/ms7m/notify-py/workflows/Test%20Windows/badge.svg">
  </p>
  <br>
  <p align="center">
    <img src="https://img.shields.io/badge/Available-on%20PyPi-blue?logoColor=white&logo=Python">
    <img src="https://img.shields.io/badge/Python-3.6%2B-blue?logo=python">
    <img src="https://img.shields.io/badge/Formatting-Black-black.svg">
  </p>
</div>


## Notify.py

notify.py is a small python module for sending native cross-platform notifications. The only dependency required is loguru.

***



## Getting started

```python
from notifypy import Notify

notification = Notify()
notification.title = "Cool Title"
notification.message = "Even cooler message."

notification.send()
```

That's it. This will send a desktop notification on the respected user platform.

***

# Installation 

```python
pip install notify-py
```

***
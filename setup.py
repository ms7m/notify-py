import io
from notifypy.cli import entry
import os
import sys

from setuptools import Command, find_packages, setup

# import notifypy

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="notify_py",
    version="0.3.0",
    author="Mustafa Mohamed",
    author_email="ms7mohamed@gmail.com",
    description="Cross-platform desktop notification library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ms7m/notify-py",
    python_requires=">=3.6.0",
    packages=find_packages(
        exclude=["testing", "*.testing", "*.testing.*", "testing.*"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "notifypy = notifypy.cli:entry"
        ]
    },
    include_package_data=True,
    install_requires=["loguru"],
)

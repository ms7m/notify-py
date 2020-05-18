
import io
import os
import sys

from setuptools import Command, find_packages, setup

import notifypy

setup(
    name="notifypy",
    version=notifypy.__version__,
    author="Mustafa Mohamed",
    author_email="ms7mohamed@gmail.com",
    python_requires=">=3.6.0",
    packages=find_packages(
        exclude=["testing", "*.testing", "*.testing.*", "testing.*"]
    ),
    include_package_data=True,
    install_requires=[
        "loguru==0.4.1"
    ]
)
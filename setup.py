# filepath: setup.py
from setuptools import setup, find_packages

setup(
    name="geocoder_kr",
    version="0.28",
    author="gisman",
    author_email="gisman@gmail.com",
    description="Python-based geocoding solution for Korean addresses",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gisman/geocoder-kr",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License-Expression:: CC-BY-NC-SA-4.0",
        "Operating System :: POSIX :: Linux",
    ],
    license="CC-BY-NC-SA-4.0",
    python_requires=">=3.6, <3.12",
    install_requires=open("requirements.txt").read().splitlines(),
)

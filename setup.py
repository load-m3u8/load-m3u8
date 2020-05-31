#!/usr/bin/env python3
""" Install packages for load_m3u8.py """

from os.path import dirname, abspath, join

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [req for req in open(abspath(join(dirname(__file__), 'requirements.txt')))]

setuptools.setup(
    name="load_m3u8",
    version="0.0.1",
    author="sunmaolin.com",
    author_email="xxdx@sunmaolin.com",
    description="Download video by m3u8 file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/16beer/load_m3u8",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

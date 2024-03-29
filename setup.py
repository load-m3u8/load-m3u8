#!/usr/bin/env python3
# _*_coding:utf-8_*_
""" Install packages for resolve.py """

from os.path import dirname, abspath, join

import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

_locals = {}
with open("src/load_m3u8/version.py", "r", encoding='UTF-8') as fp:
    exec(fp.read(), None, _locals)
version = _locals["__version__"]

install_requires = [req for req in open(abspath(join(dirname(__file__), 'requirements.txt')))]

setuptools.setup(
    name="load_m3u8",
    version=version,
    author="sunmaolin.com",
    author_email="dev@sunmaolin.com",
    description="Download video by m3u8 file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/16beer/load_m3u8",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=install_requires,
    license="Apache License",
    platforms='any',
    test_suite='tests',
    keywords='m3u8 m3u8-downloader m3u8-download',
    entry_points={
        'console_scripts': ['load-m3u8 = load_m3u8.load.__main__:main', 'gen-m3u8 = load_m3u8.generate.__main__:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

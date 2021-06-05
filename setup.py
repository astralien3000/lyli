#!/usr/bin/env python

from distutils.core import setup

setup(
    name="lyli",
    version="0.0.1",
    description="Lyli programming language",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/astralien3000/lyli",
    author="Loïc Dauphin",
    author_email="astralien3000@yahoo.fr",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["lyli"],
    include_package_data=True,
    requires=[
        "lark",
    ],
    entry_points={"console_scripts": ["lyli=lyli.__main__:main"]},
)

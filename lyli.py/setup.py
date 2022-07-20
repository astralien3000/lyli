from distutils.core import setup
from os import path

def get_long_description():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

setup(
    name="lyli",
    version="0.0.1",
    description="Lyli programming language",
    long_description=get_long_description(),
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
    package_dir={"": "src"},
    packages=["lyli"],
    include_package_data=True,
    install_requires=[
        "lark",
    ],
    entry_points={
        "console_scripts": [
            "lyli=lyli.__main__:main",
        ],
    },
)

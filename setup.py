from setuptools import setup
from plof import __version__

setup(
    name='plof',
    version=__version__,
    packages=['plof'],
    description='Plottext Command Line Utility',
    author="Jack Mead",
    url="",
    entry_points={
        "console_scripts": {
            "plof=plof.main:main"
        }
    },
    install_requires=[
        'plotext>=4.0.0; python_version >= "3"',
        'jq>=1.2.1; python_version >= "3"',
    ]
)
"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


APP = ['EasySync.py']
DATA_FILES = [('', ['icon']),('', ['README.md'])]
OPTIONS = {
    'iconfile': 'icon/EasySync.icns'
}
#'argv_emulation': True}

setup(
    name='EasySync',
    version='0.2-beta',
    description='A simple and safe utility to synchronise a copy of working files',
    long_description=long_description,
    url='https://github.com/moaxey/EasySync',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Archiving :: Mirroring',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='desktop backup utility',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

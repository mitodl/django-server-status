# -*- encoding: utf-8 -*-
"""
Python setup file for the server_status app.

In order to register your app at pypi.python.org, create an account at
pypi.python.org and login, then register your new app like so:

    python setup.py register

If your name is still free, you can now make your first release but first you
should check if you are uploading the correct files:

    python setup.py sdist

Inspect the output thoroughly. There shouldn't be any temp files and if your
app includes staticfiles or templates, make sure that they appear in the list.
If something is wrong, you need to edit MANIFEST.in and run the command again.

If all looks good, you can make your first release:

    python setup.py sdist upload

For new releases, you need to bump the version number in
server_status/__init__.py and re-run the above command.

For more information on creating source distributions, see
http://docs.python.org/2/distutils/sourcedist.html

"""
from __future__ import unicode_literals
import os
from setuptools import setup, find_packages
import server_status as app

# pylint: disable=invalid-name
install_requires = open('requirements.txt').read().splitlines()


def read(filename, is_restructured_text=False):
    """Helper function to read bytes from file"""
    try:
        text = open(os.path.join(os.path.dirname(__file__), filename)).read()
        if is_restructured_text:
            # See https://packaging.python.org/specifications/core-metadata/#description
            # any newline has to be suffixed by 7 spaces and a pipe character
            text = text.replace("\n", "\n       |")
        return text
    except IOError:
        return ''


setup(
    name="django-server-status",
    version=app.__version__,
    description=read('DESCRIPTION'),
    long_description="",  # temporarily removed, but it would be located at README.rst
    license='The AGPL License',
    platforms=['OS Independent'],
    keywords='django, monitoring, health check',
    author='MIT Office of Digital Learning',
    author_email='mitx-devops@mit.edu',
    url="https://github.com/mitodl/django-server-status",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["django"] + install_requires,
)

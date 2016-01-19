"""
These settings are used by the ``manage.py`` command.

With normal tests we want to use the fastest possible way which is an
in-memory sqlite database but if you want to create South migrations you
need a persistant database.

Unfortunately there seems to be an issue with either South or syncdb so that
defining two routers ("default" and "south") does not work.

"""
from __future__ import unicode_literals
from distutils.version import StrictVersion  # pylint: disable=import-error, no-name-in-module

import django

from server_status.tests.test_settings import *  # pylint: disable=wildcard-import, unused-wildcard-import


django_version = django.get_version()  # pylint: disable=invalid-name
if StrictVersion(django_version) < StrictVersion('1.7'):
    INSTALLED_APPS.append('south', )


BROKER_URL = 'redis://redis:6379/4'
CELERY_RESULT_BACKEND = 'redis://redis:6379/4'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'db',
        'PORT': '5432',
    }
}
HAYSTACK_CONNECTIONS = {
    'default': {
        'URL': 'http://elastic:9200',
        'INDEX_NAME': 'haystack',
    }
}

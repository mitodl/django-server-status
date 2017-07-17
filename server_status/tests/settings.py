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
import os
import logging

import django

DEBUG = True

logging.getLogger("factory").setLevel(logging.WARN)

SITE_ID = 1

APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
        'PORT': '5432',
    }
}

ROOT_URLCONF = 'server_status.tests.urls'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(APP_ROOT, '../app_static')
MEDIA_ROOT = os.path.join(APP_ROOT, '../app_media')
STATICFILES_DIRS = (
    os.path.join(APP_ROOT, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(APP_ROOT, 'tests/test_app/templates'),
)

EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
]

INTERNAL_APPS = [
    'server_status',
    'server_status.tests.test_app',
]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(
    os.path.join(APP_ROOT, 'tests/coverage'))
COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'settings$', 'urls$', 'locale$',
    'migrations', 'fixtures', 'admin$', 'django_extensions',
]
COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS

SECRET_KEY = 'foobar'

ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL', 'http://127.0.0.1:9200')

USE_CELERY = True
STATUS_TOKEN = 'asdf'

BROKER_URL = os.environ.get('BROKER_URL', 'redis://127.0.0.1:6379/4')
CELERY_RESULT_BACKEND = BROKER_URL

HEALTH_CHECK = ['REDIS', 'ELASTIC_SEARCH', 'POSTGRES', 'CELERY']


django_version = django.get_version()  # pylint: disable=invalid-name
if StrictVersion(django_version) < StrictVersion('1.7'):
    INSTALLED_APPS.append('south', )

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

BROKER_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/4')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@127.0.0.1:5672/')
CELERY_RESULT_BACKEND = BROKER_URL

HEALTH_CHECK = ['REDIS', 'ELASTIC_SEARCH', 'POSTGRES', 'CELERY']
# A test certificate
MIT_WS_CERTIFICATE = """
-----BEGIN CERTIFICATE-----
MIIDODCCAiACCQCVPqAVIXIUBDANBgkqhkiG9w0BAQsFADBeMQswCQYDVQQGEwJV
UzELMAkGA1UECAwCTUExEjAQBgNVBAcMCUNhbWJyaWRnZTEMMAoGA1UECgwDTUlU
MQwwCgYDVQQLDANPREwxEjAQBgNVBAMMCW1pdC5sb2NhbDAeFw0xODA5MTgxMjU5
MTZaFw0xOTA5MTgxMjU5MTZaMF4xCzAJBgNVBAYTAlVTMQswCQYDVQQIDAJNQTES
MBAGA1UEBwwJQ2FtYnJpZGdlMQwwCgYDVQQKDANNSVQxDDAKBgNVBAsMA09ETDES
MBAGA1UEAwwJbWl0LmxvY2FsMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKC
AQEAzh5L0oNqmMv1kGmSXLHJSxo7gaf4Fr3Ty6xuvEau75Fr6VhXkeiU+f4wy6GY
7rpjTCOjXWtHzkomePFwHuTncIJzudX//kLxm2sakBtxV7EWzbR7qqPSEOCi1CDx
ST3Fn5pA3Fz3X4kq6IZ6rj3V+4xFRjjTYzChkCCMiamyWEYUXvLlMWX5I7zVtEJM
d8LdygJHXvMHL5SXM1rx9ecws4aN0v5NHitOduvkNiiiUpBfc+223Gy4ewBHpwiZ
xW03YZRP0fVW8HjLrq1Qz3COXD79w9IUzHV+3MhCRIVfiiJB6uJrYTYKQtTY1U7U
BVn6X3PTA3eKNLFRo0xl7S5WdQIDAQABMA0GCSqGSIb3DQEBCwUAA4IBAQASZzHi
ubyb/3A2KnH2FoydNIIbKOz4j2x5+esFebweY4GdLKQVW0RPfwoZJ8nX2QUJZN0V
mTXf9i1W379h5P6m0yb2Z2KyoDIzIbOgSjHPZX6qKmL+4Td46C8IOn0IEGKrJhHT
mF9sznmFY6CodorYwP1S384UcZJ+zPHVRJre93MFp1JIiDXppuquZQctbbrSyrme
5y32wk0NZNurSt9v0pWLqw4LWgZC5NIDPsHadU3OcUc3QE4BGSxDO6l40Rtib56S
NBoBmw0qtQMytHY7XzbDQnfeUC3l0pGPElliO/e0QmEWTaSpKhIfox9BcZgGODxo
mr30JWxtXMonum5h
-----END CERTIFICATE-----"""

django_version = django.get_version()  # pylint: disable=invalid-name
if StrictVersion(django_version) < StrictVersion('1.7'):
    INSTALLED_APPS.append('south', )

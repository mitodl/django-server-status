django-server-status
====================

Monitor server status with a healthcheck.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-server-status

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/mitodl/django-server-status.git#egg=django-server-status

Add a stanza like this to your settings. Current supported services are 'REDIS', 'ELASTIC_SEARCH', 'POSTGRES', 'CELERY'.

.. code-block:: python

    HEALTH_CHECK = ['REDIS', 'ELASTIC_SEARCH', 'POSTGRES']


Add ``server_status`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'server_status',
    )

Add the ``server_status`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^status/', include('server_status.urls')),
    )


Release Notes
-------------

0.3: Added status_all property to the status results JSON.
0.2: Support for celery validation.
0.1.1: Included tests
0.1: Initial Release

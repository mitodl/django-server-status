server-status
============

Monitor server status with a healthcheck.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install server-status

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/mitodl/server-status.git#egg=server_status

Add a stanza like this to your settings. True means it will be checked. False means it will not be.

.. code-block:: python

    HEALTH_CHECK = {
        'REDIS': True,
        'ELASTIC_SEARCH': True,
        'POSTGRES': True,
    }


Add ``server_status`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'server_status',
    )

Add the ``server_status`` URLs to your ``urls.py``

.. code-block:: python

    from server_status.views import status
    urlpatterns = patterns('',
        ...
        url(r'^status', status, name='status'),
    )

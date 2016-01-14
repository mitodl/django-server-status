"""URLs for the server_status app."""
from compat import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$',
        views.status,
        name='status'),
)

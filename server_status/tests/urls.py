"""URLs to run the tests."""
from compat import patterns, include, url
from django.contrib import admin
from server_status.views import status

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^status', status, name='status')
)

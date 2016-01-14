"""URLs to run the tests."""
from compat import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^status', include('server_status.urls')),
)

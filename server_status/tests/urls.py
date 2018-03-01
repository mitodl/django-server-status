"""URLs to run the tests."""
from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = (
    url(r'^admin/', admin.site.urls),
    url(r'^status', include('server_status.urls')),
)

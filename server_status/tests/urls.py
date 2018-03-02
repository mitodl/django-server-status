"""URLs to run the tests."""
try:
    from django.urls import include
except ImportError:
    from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

admin.autodiscover()

urlpatterns = (
    url(r'^admin/', admin.site.urls),
    url(r'^status', include('server_status.urls')),
)

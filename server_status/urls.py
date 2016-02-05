"""URLs for the server_status app."""
from django.conf.urls import url

from server_status import views


urlpatterns = (
    url(r'^$', views.status, name='status'),
)

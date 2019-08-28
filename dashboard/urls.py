from django.conf.urls import url
from . import dashboard

urlpatterns = [
    url(r'^$', dashboard.Dashboard.as_view(), name='index'),
]

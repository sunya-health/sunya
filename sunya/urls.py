"""sunya URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from sunya import main

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^account/', include('account.urls')),
    url(r'^security/', include('security.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^$', main.MainPage.as_view(), name='main'),
    url(r'^sunya/$', main.HealthList.as_view(), name='health_add'),
    url(r'^sunya/(?P<pk>[0-9]+)/$', main.HealthDetails.as_view(), name='health_get'),
    url(r'^sunya/organization/$', main.OrganizationDetails.as_view(), name='organization'),
    url(r'^sunya/organization/user/$', main.AssignOrCreateUser.as_view(), name='assign_user'),
    url(r'^settings/', include('settings.urls')),
]

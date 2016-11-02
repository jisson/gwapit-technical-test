"""gwapit_technical_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from gwapit.views import IndexView
from gwapit.views import LogoutView
from gwapit.views import email_list, get_email_message

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # Python social urls
    url('^soc/', include('social.apps.django_app.urls', namespace='social')),

    # Api views
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^api/v1/resource/emails/$', email_list, name='emails'),
    url(r'^api/v1/resource/emails/(?P<message_id>[\w-]+)/$', get_email_message, name='get_email_message'),

    # Single page application
    url('^.*$', IndexView.as_view(), name='index'),

]
urlpatterns = format_suffix_patterns(urlpatterns)

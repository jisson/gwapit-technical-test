from django.conf.urls import patterns, url
from gwapit.views import LogoutView, email_list, get_email_message

__author__ = 'Pierre Rodier | pierre@buffactory.com'


urlpatterns = patterns('gwapit.views',

                       # Authentication urls
                       url(r'auth/logout/$', LogoutView.as_view(), name='logout'),

                       # Resource urls
                       url(r'resource/emails/$', email_list, name='emails'),
                       url(r'resource/emails/(?P<message_id>[\w-]+)/$', get_email_message, name='get_email_message'),
                       )

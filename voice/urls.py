from django.conf.urls.defaults import *

urlpatterns = patterns('voice',
        url(r'^static/(?P<path>.*)$', 'views.static_media',
            name='voice-media'),

        url(r'^$', 'views.index', name='voice-index'),
        url(r'^admin/', 'views.admin', name='voice-admin'),
        )

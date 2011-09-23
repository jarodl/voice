from django.conf.urls.defaults import *

urlpatterns = patterns('voice',
        url(r'^static/(?P<path>.*)$', 'views.static_media',
            name='voice-media'),

        url(r'^$', 'views.index', name='voice-index'),
        url(r'^features/(?P<feature_id>\d+)$', 'views.feature',
        name='voice-feature'),
        url(r'^features/new/', 'views.new_feature', name='voice-new-feature'),
        url(r'^admin/', 'views.admin', name='voice-admin'),
        )

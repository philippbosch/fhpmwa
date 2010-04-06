import os.path

from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_ROOT, 'media')}),
    (r'^admin/', include(admin.site.urls)),
    url(r'^jssettings/$', 'django.views.generic.simple.direct_to_template', {'template': 'jssettings.js', 'mimetype': 'application/x-javascript', 'extra_context': {'settings':settings}}, name="jssettings"),
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'app.html',}),
    (r'^people/', include('fhpmwa.people.urls')),
    
    url(r'^events/$', 'django.views.generic.simple.direct_to_template', {'template': 'touchevents.html',}),
    url(r'^multitouch/$', 'django.views.generic.simple.direct_to_template', {'template': 'multitouch.html',}),
)

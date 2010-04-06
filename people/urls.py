from django.conf.urls.defaults import *

urlpatterns = patterns('fhpmwa.people.views',
    url(r'^$', 'people_list', name="people_list"),
    url(r'^stats/$', 'people_stats', name="people_stats"),
    url(r'^register/$', 'register', name="people_register"),
) + patterns('', 
    url(r'^register/done/$', 'django.views.generic.simple.direct_to_template', {'template':'people/register-done.html'}, name="people_register_done"),
)

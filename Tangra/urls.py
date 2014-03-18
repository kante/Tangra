from django.conf.urls import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from Tangra.studies.views import *
from Tangra.views import *
#from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Libraries
    
    url(r'^$', 'Tangra.views.home', name="home"),
    (r'^admin/', include(admin.site.urls)),
    (r'^study/', include('Tangra.studies.urls')),
    
    url(r'^accounts/login/$',  login, name="login"),
    url(r'^accounts/logout/$', logout, name="logout"),
    
    # Study builder UI
    url(r'^study_builder/', include('study_builder.urls')),
    # Studies generated by build_study.py script should be matched by this
    url(r'^user_studies/', include('user_studies.urls')),
    
    # Video conferencing test 
    url(r'^video_conferencing/', include('Tangra.investigator.video_conferencing.urls')),
    
    # New investigator interface
    url(r'^investigator/', include('Tangra.investigator.urls')),
    
    # All the functions required to run a study are in here
    url(r'^exe_interface/', include('Tangra.public_api.urls')),
    
)


if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.MEDIA_ROOT }),
    )


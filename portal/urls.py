from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from portal.studies.views import *
from portal.views import *
#from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Libraries
    (r'^tinymce/', include('tinymce.urls')),
    
    url(r'^$', 'portal.views.home', name="home"),
    (r'^admin/', include(admin.site.urls)),
    (r'^study/',include('portal.studies.urls')),
    
    
    url(r'^accounts/login/$',  login, name="login"),
    url(r'^accounts/logout/$', logout, name="logout"),
    
    
    # Study builder UI
    url(r'^study_builder/', include('portal.study_builder.urls')),
    # Studies generated by build_study.py script should be matched by this
    url(r'^user_studies/', include('portal.user_studies.urls')),
    
    # Video conferencing test 
    url(r'^video_conferencing/', include('portal.investigator.video_conferencing.urls')),
    
    # New investigator interface
    url(r'^investigator/', include('portal.investigator.urls')),
    
    
)


if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.MEDIA_ROOT }),
    )


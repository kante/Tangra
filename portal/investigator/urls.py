from django.conf.urls.defaults import *
from portal.investigator.views import *

urlpatterns = patterns('', 
                       url(r'^$', investigator_home, name='investigator_home'),
                       url(r'^(?P<sort_by>[a-z_]+)$', investigator_home, name='investigator_home'),
                       url(r'^view_user/(?P<user>[a-zA-Z0-9_]+)$', view_user, name='user_inspector'),
                      )

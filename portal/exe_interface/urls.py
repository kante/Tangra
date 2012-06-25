from django.conf.urls.defaults import *
from portal.exe_interface.views import *


urlpatterns = patterns('',
    url(r'^$', testing, name="testing"),
    url(r'^login$', login, name="login")
)


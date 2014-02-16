from django.conf.urls import *
from views import *

urlpatterns = patterns('', 
                       #url(r'^$', basic_test, name='basic_test'),
                       url(r'^invite_user.*$', invite_user, name='invite_user'),
                       url(r'^uninvite_user.*$', uninvite_user, name='uninvite_user'),
                       url(r'^decline_video_request.*$', decline_video_request, name='decline_video_request')
                       
                      )


from django.conf.urls.defaults import *
from portal.user_studies.views import *

urlpatterns = patterns('', url(r'^example_study/welcome_page$', welcome_page, name='welcome_page'), url(r'^example_study/simple_task$', simple_task, name='simple_task'), url(r'^example_study/bye_page$', bye_page, name='bye_page'))
    
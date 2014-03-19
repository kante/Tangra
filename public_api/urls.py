from django.conf.urls import *
from public_api.views import *


urlpatterns = patterns('',
    url(r'^login$', login, name="login"),
    url(r'^logout$', logout, name='logout'),
    
    url(r'^get_current_stage$', get_current_stage, name='get_current_stage'),
    
    url(r'^save_data$', save_data, name='save_data'),
    url(r'^get_data$', get_data, name='get_data'),
    
    
    url(r'^save_data_with_key$', save_data_with_key, name='save_data_with_key'),
    url(r'^get_data_for_key$', get_data_for_key, name='get_data_for_key'),
    url(r'^get_data_for_stage_and_key$', get_data_for_stage_and_key, name='get_data_for_stage_and_key'),
    
    url(r'^upload_file$', upload_file, name='upload_file'),
    
    url(r'^finish_current_stage$', finish_current_stage, name='finish_current_stage'),
    
    # The older name for things. We will phase this out before wednesday.
    url(r'^get_current_stage_info$', get_current_stage_info, name="get_current_stage_info"),
    url(r'^get_user_data$', get_user_data, name="get_user_data")
    
    
)


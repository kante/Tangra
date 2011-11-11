from django.conf.urls.defaults import *
from portal.studies.views import *

urlpatterns = patterns('',
    url(r'^$', show_many_studies, name="show_many_studies"),
    url(r'^send-data$', log_game, name="log_game"),   
    url(r'^mark-read$', mark_read, name="mark_read"),   
    url(r'^ic$', informed_consent, name="informed_consent"), # send people here for informed consent
    url(r'^consented$', consented, name="consented"),
    url(r'^datadump/(\d+)$', data_dump, name="data_dump"),
    
    
    url(r'^choose_task$', choose_task, name="choose_task"),
    url(r'^alert_send$', send_alert, name="send_alert"),
    url(r'^quest$', questionnaire, name="questionnaire"),
    
    
    url(r'^fsess$', finish_session, name="finish_session"),
    url(r'^(\d+)/(\d+)$', show_one_study, name="show_one_study"),
    
    
    # General function to store arbitrary JSON strings from a user study
    url(r'^save_post_data$', save_post_data, name="save_post_data"),
    
    (r'^tinymce/', include('tinymce.urls')), 

)

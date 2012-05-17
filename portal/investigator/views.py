from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from portal.studies.models import User, Study, UserStage, Data, StudyParticipant
from video_conferencing import *


def get_progress(user, study):
    """
    """
    studypart = study.get_study_participant(user)
    stages = UserStage.objects.filter(user=user, study=study)
    #stages = studypart.participant_stages()
    current_stage = studypart.get_current_stage()
    
    #print stages, current_stage
    colors = ["green", "orange", "grey"]
    return [colors[stage.status] for stage in stages]


def is_online(user):
    return True if cache.get(user.username) else False

def is_late(user):
    current_stages = UserStage.objects.filter(user=user, status=1)
    return reduce(lambda x, y : x or y.overdue(), current_stages, False)

def build_user_data(participants, study, sort_by):
    user_data = []
    for user in participants:
        
        data = {
                    "username":user.username, 
                    "is_online":is_online(user),
                    "progress":get_progress(user, study),
                    "is_late":is_late(user)
                }
                
        user_data.append(data)
    
    if sort_by == "username":
        key_fcn = lambda user:user["username"]
    elif sort_by == "is_online":
        key_fcn = lambda user: not user["is_online"]
    elif sort_by == "is_late":
        key_fcn = lambda user: not user["is_late"]
    
    user_data.sort(key=key_fcn)
    
    return user_data


@login_required
def investigator_home(request, sort_by="username"):
    online_users = get_online_users()
    
    
    # build a dictionary of participants in this investigators studies
    my_studies = {}
    for s in Study.objects.all():
        for i in s.investigators.all():
            if request.user == i:
                my_studies[s] = build_user_data(s.participants.all(), s, sort_by)
    
    
    request_declined = True if cache.get(request.user.username + "_no_chat_requested") else False
    
    return render_to_response('investigator_home.html', locals(), 
                              context_instance=RequestContext(request))


#@login_required
def view_user(request, user):
    username = user
    user_object = User.objects.get(username=user)
    sps = StudyParticipant.objects.filter(user=user_object)
    
    raw_user_data = []
    user_data = {}
    
    # for each study-participant entry
    # - ensure study's name has a placeholder in user_data dict
    # - dump raw data in raw_user_data list
    for sp in sps:
        if sp.study.name not in user_data:
            user_data[sp.study.name] = []
        raw_user_data.extend(Data.objects.filter(studyparticipant=sp))
    
    # go over raw data and organize it in user_data dict by study name
    for datum in raw_user_data:
        the_study = datum.studyparticipant.study.name
        next_data = {"stage":datum.stage, "stub":datum.stage_stub, "timestamp":datum.timestamp, "data":datum.datum}
        user_data[the_study].append( next_data )
    
    # print user_data
    
    # create a new opentok session 
    # TODO: put the below things in settings.py and document how to set them
    api_key = "9550782"        
    api_secret = "3a9bc01e5217c49d7f710a1324c4ed520bcdc26c"  
    session_address = "64.230.48.65" 
    
    opentok_sdk = OpenTokSDK.OpenTokSDK(api_key, api_secret)
    #session_properties = {OpenTokSDK.SessionProperties.p2p_preference: "disabled"}
    #session = opentok_sdk.create_session(session_address, session_properties)
    #session_id =  session.session_id
    #token = opentok_sdk.generate_token(session_id, OpenTokSDK.RoleConstants.PUBLISHER, None, None)
    
    session_id = "1_MX45NTUwNzgyfjY0LjIzMC40OC42NX4yMDExLTEyLTEyIDE5OjA0OjQ2Ljc0NTE1MCswMDowMH4wLjYzOTc2NDcyMjk1MX4"
    token = opentok_sdk.generate_token(session_id, OpenTokSDK.RoleConstants.PUBLISHER, None, None)
    
    return render_to_response('user_viewer.html', locals(), 
                              context_instance=RequestContext(request))



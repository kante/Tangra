from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from portal.studies.models import User, Study, UserStage
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


def build_user_data(participants, study, sort_by):
    user_data = []
    for user in participants:
        data = {
                    "username":user.username, 
                    "is_online":is_online(user),
                    "progress":get_progress(user, study),
                    "is_late":user.username == "guy_J" or user.username == "mr_A"
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
    
    
    # create a new opentok session 
    
    
    return render_to_response('investigator_home.html', locals(), 
                              context_instance=RequestContext(request))


@login_required
def view_user(request, user):
    user_data = {"username":user}
    user_object = User.objects.get(username=user)
    user_stages = UserStage.objects.filter(user=user_object)
    print user_stages
    return render_to_response('user_viewer.html', locals(), 
                              context_instance=RequestContext(request))



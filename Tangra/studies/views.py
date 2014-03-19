import sys
from django.shortcuts import render_to_response
from django.template import RequestContext
import hashlib

from sys import stderr 

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from models import *
from forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from context_processors import *
import datetime
from django.core.cache import cache


from Tangra.investigator.video_conferencing import OpenTokSDK


############### Study


@login_required
def show_many_studies(request):
    studies_as_participant = StudyParticipant.objects.filter(user=request.user)
    current_stages = UserStage.objects.filter(user=request.user, status=1)
        
    print >>stderr,  current_stages
    
    return render_to_response('study/show_many_studies.html', locals(), context_instance=RequestContext(request))


@login_required
def show_one_study(request,as_inv,s_id):
    # Find a better way to do the study finding stuff???
    study_id = int(s_id)
    request.session['study_id'] = study_id
    study = Study.objects.get(id=study_id)
    video_request = True if cache.get(request.user.username + "_has_pending_invite") else False
    username = request.user.username
    
    (api_key, session_id, token) = ("", "", "")
    if video_request:
        # TODO: not repeat this stuff... put it in the video_conferencing module dumbass
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
        
    studypart = study.get_study_participant(request.user)
    stages = UserStage.objects.filter(user=request.user, study=study)
    
    current_stage = studypart.get_current_stage()
    if current_stage:
        action = current_stage.stage.url
        return render_to_response('study/show_one_study.html',locals(), context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/study/')


############### Data Collection


@login_required
def informed_consent(request):
    sid = request.session['study_id']
    study = Study.objects.get(id=sid)
    role = study.role(request.user)
    if role > -1:
        #participant
        
        # CLEANUP: this chain of lookups seems unnecessary
        studynum = sid
        studypart = study.get_study_participant(request.user)
        stage = studypart.get_current_stage()
        action = stage.stage.url
        if stage.order != 1:
            return HttpResponseBadRequest()
    else: 
        #unauthorized URL mucking about with
        return HttpResponseBadRequest()
    return render_to_response('study/informed_consent.html',locals(), context_instance=RequestContext(request))


@login_required
def questionnaire(request):
    if request.method == 'POST':
        form = QForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            log(request,"QUE",cd)
            return HttpResponseRedirect('/study/0/'+ str(request.session['study_id']))
    else:
        form = QForm()
    return render_to_response('study/questionnaire.html', {'form': form, 'button': 'Submit'})


@login_required
def consented(request):
    study_id = int(request.session['study_id'])
    study = Study.objects.get(id=study_id)
    
    #participant
    studypart = study.get_study_participant(request.user)
    stage = studypart.get_current_stage()
    log(request, "CON", "Consent Given")
    stage.session_completed()
    
    return HttpResponseRedirect('/study/0/'+str(study_id))


@login_required
def finish_session(request):
    # TODO: Find a better way to determine what session you're in...

    study_id = request.session['study_id']
    study = Study.objects.get(id=study_id)

    studypart = StudyParticipant.objects.get(study=study,user=request.user)
    #stage = studypart.get_current_stage()
    stage = UserStage.objects.get(user=request.user, study=study, status=1)
    stage.increase_stage_count()
    
    return HttpResponseRedirect('/study/0/'+str(study_id))


@login_required
def finish_infinite_session(request):
    study_id = request.session['study_id']
    study = Study.objects.get(id=study_id)
    stage = UserStage.objects.get(user=request.user, study=study, status=1)
    stage.session_completed()
    
    return HttpResponseRedirect('/study/0/'+str(study_id))


# def cheat_finish_session(request):
#     study_id = request.GET['study_id']
#     study = Study.objects.get(id=study_id)
# 
#     studypart = StudyParticipant.objects.get(study=study,user=request.GET['user_id'])
#     #stage = studypart.get_current_stage()
#     stage = UserStage.objects.get(user=request.user, study=study, status=1)
#     stage.session_completed()
# 
#     return HttpResponseRedirect('/study/0/'+str(study_id))



@login_required
def save_post_data(request):
    """Saves arbitrary POST data from a user stage and responds with a 
    confirmation."""
    
    if request.method != 'POST': 
        return HttpResponse("not_post")
        
    studyid = request.session['study_id']
    
    # Save in comma separated value format
    data = ""
    for key in request.POST:
        data = data + "{0},{1}\n".format(key, request.POST[key])
    
    #print >>sys.stderr, data
    #TODO: how to print to stderr without crashing shit?
    print data
    
    dt = datetime.datetime.now()    
    code = "CSV"
    
    log(request, code, data)
    
    #send: studyid, request.user, time, data
    return HttpResponse("success")


@login_required
def log(request, code, datum):
    """Logs things"""
    #print >>sys.stderr, "logging"
    studyid = request.session['study_id']
    
    try:
        Data.write(studyid, request.user, datetime.datetime.now(), code, datum)
    except Exception:
      print "logging: failed"
     #send: studyid, request.user, time, data
    return HttpResponse("YAY!")





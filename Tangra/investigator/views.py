from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.core.servers.basehttp import FileWrapper
from django import forms        
from zipfile import ZipFile
from StringIO import StringIO
import json
import os
import sys 

from Tangra.studies.models import User, Study, UserStage, Data, StudyParticipant, Group, StageGroup
from video_conferencing import *
from Tangra.users.models import UserRoles
import datetime


def add_user_to_db(study_id, group, user, password):
    study = Study.objects.get(id=study_id)
    user.set_password(password)
    user.save()
    
    # now update the user profile (it should be created after the save)
    profile = user.get_profile()
    profile.user_role = UserRoles.PARTICIPANT
    profile.save()
    study.participants.add(user)
    group = Group.objects.get(study=study_id, name=group)
    
    try:
        study_participant = StudyParticipant.objects.get(study=study, user=user, group=group)
    except StudyParticipant.DoesNotExist:
        study_participant = StudyParticipant(study=study, user=user, group=group)
    study_participant.save()
    
    stagegroups = StageGroup.objects.filter(group=group)
    
    for stagegroup in stagegroups:
        stage = stagegroup.stage
        
        #add a UserStage for each user/stage pair
        try:
            user_stage = UserStage.objects.get(stage=stagegroup.stage, user=user, order=stagegroup.order, study=study_id)
        except UserStage.DoesNotExist:
            user_stage = UserStage(stage=stagegroup.stage, user=user, order=stagegroup.order, \
                study=study, stage_times_completed=0, stage_times_total=stagegroup.stage_times_total, \
                custom_data=stagegroup.custom_data)
        
        # set all status to incomplete
        user_stage.status = 1 if stagegroup.order == 0 else 2
        user_stage.sessions_completed = 0
        user_stage.start_date = datetime.datetime.now()
        user_stage.save()


def add_user(request, study_id):
    alert = ""
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        group = request.POST['group']
    else:
        # Strange request. Send them back to the start
        return HttpResponse("Strange request... not POST!?")
        
    
    # check to see if the user exists, retry if it does
    try:
        user = User.objects.get(username=username)
        error = True
        error_msg = "User already exists. Try a different username."
        groups = [group]
        return render_to_response('add_user_form.html', locals(), context_instance=RequestContext(request))
    except User.DoesNotExist:
        user = User(username=username)
    
    add_user_to_db(study_id, group, user, password)
    
    return HttpResponseRedirect('/investigator/', locals())
    


def add_user_form(request, study_id):
    groups = [g.name for g in Group.objects.filter(study=study_id)]
    
    return render_to_response('add_user_form.html', locals(), 
                              context_instance=RequestContext(request))



def get_progress(user, study):
    """
    """
    studypart = study.get_study_participant(user)
    stages = UserStage.objects.filter(user=user, study=study)
    #stages = studypart.participant_stages()
    current_stage = studypart.get_current_stage()
    
    #print >>sys.stderr, stages, current_stage
    
    colors = ["green", "orange", "grey"]
    return [
        [colors[stage.status], stage.stage_times_completed, stage.stage_times_total] 
        for stage in stages
        ]
        


def is_online(user):
    return True if cache.get(user.username) else False


def is_late(user):
    current_stages = UserStage.objects.filter(user=user, status=1)
    return reduce(lambda x, y : x or y.overdue(), current_stages, False)


def get_data(request):
    
    study_data = {}
    
    if request.method == u'GET':
        GET = request.GET
        
        if GET.has_key(u'progressUsers[]') and GET.has_key(u'study'):
            progressUsers = GET.getlist(u'progressUsers[]')
            study = GET[u'study']
            
            # get pertinent user data, serialize it and offer file to download
            study_data = get_study_data(study, progressUsers)
        
    jsonResponse = json.dumps(study_data, sort_keys=True, indent=4, cls=DjangoJSONEncoder)
    
    response = HttpResponse(jsonResponse, mimetype='application/json')
    response['Content-Disposition'] = 'attachment; filename=study_data.txt'
    return response
    
    
def download_file(request):
    
    if request.method == u'GET':
        
        GET = request.GET
        
        if GET.has_key(u'fileUser') and GET.has_key(u'fileName'):
            fileUser = GET[u'fileUser']
            fileName = GET[u'fileName']
            
            filePath = os.path.join(USER_FILES, fileUser, fileName)
            
            print >>sys.stderr,  "ASDFASDF", filePath

            if os.path.isfile(filePath):
                wrapper = FileWrapper(file(filePath))
                response = HttpResponse(wrapper, mimetype='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename=' + fileName
                return response
                
            else:
                print >>sys.stderr,  "No file called '" + fileName + "' found for user '" + fileUser + "'."


def download_files(request):
    
    if request.method == u'POST':
        
        POST = request.POST
        
        # process querydict to a regular dictionary
        postDict = post2dict(POST)
        
        # create file in memory and create a zip file with it
        inMemoryOutputFile = StringIO()
                
        # working from memory
        zipFile = ZipFile(inMemoryOutputFile, 'w')
        
        for user in postDict:
            # find user file dir
            userPath = os.path.join(USER_FILES, user)
            
            # if all and if user directory exists, include all files
            if postDict[user]['all'] == 1:
            
                # initialize fileList to empty list
                postDict[user]['fileList'] = []
            
                # if directory exists
                if os.path.isdir(userPath):
                    # list all files
                    userFiles = os.listdir(userPath)
        
                    # remove from list if directory or hidden file
                    userFiles = [x for x in userFiles if not (x.startswith('.') or os.path.isdir(x))]
                
                    # substitute fileList with files in user dir
                    postDict[user]['fileList'] = userFiles
                    
            # zip files in fileList
            for f in postDict[user]['fileList']:
                
                # put each file in a user dir
                filePath = os.path.join(userPath, f)
                zipPath = os.path.join(user , f)
                zipFile.write(filePath, zipPath)
        
        # close zip
        zipFile.close()
        
        # rewind memory stringIO
        inMemoryOutputFile.seek(0)
        
        # use file wrapper for response
        wrapper = FileWrapper(inMemoryOutputFile)
        
        # no file wrapper
        # response = HttpResponse(inMemoryOutputFile, mimetype='application/octet-stream')
        
        # form and return response
        response = HttpResponse(wrapper, mimetype='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=user_files.zip'
        return response


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
    user_data = get_user_data(user)
    user_files = list_user_files(user)
    
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


def get_user_data(user):
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
    
    # print >>sys.stderr,  user_data
    return user_data


def get_study_data(study, users):

    study_object = Study.objects.get(id = study)
    study_data = {}
    
    for u in users:
        
        raw_study_data = []
        
        # print >>sys.stderr,  u
        
        user_object = User.objects.get(username=u)
        
        sps = StudyParticipant.objects.filter(user=user_object, study=study_object)
        
        for sp in sps:
            if sp.user not in study_data:
                study_data[sp.user.username] = []
            raw_study_data.extend(Data.objects.filter(studyparticipant=sp))
            
             
        for datum in raw_study_data:
            the_user = datum.studyparticipant.user
            next_data = {"stage":datum.stage, "stub":datum.stage_stub, "timestamp":datum.timestamp, "data":datum.datum}
            study_data[the_user.username].append( next_data )
            
    return study_data


def post2dict(post):
    
    postDict = {}
    
    for userKey, data in post.lists():
        
        # cleanup percent encoding
        userKey = userKey.replace('%5B', '[')
        userKey = userKey.replace('%5D', ']')
        
        userKeySplit = str(userKey).split('[')
        
        # first split string is always user
        user = userKeySplit[0]
        
        # second split string is always key and a closing bracket
        key = userKeySplit[1][:-1]
        
        # add user to dictionary if not already there
        if user not in postDict:
            postDict[user] = {}
        
        # turn data into integer
        if key == 'all':
            data = int(data[0])
            
        # create user subdictionary entry 
        postDict[user][key] = data
        
    return postDict


def list_user_files(user):
    
    userPath = os.path.join(USER_FILES, user)
    
    if os.path.isdir(userPath):
        filesDir = os.listdir(userPath)
        
        # remove if directory or hidden file
        filesDir = [x for x in filesDir if not (x.startswith('.') or os.path.isdir(x))]
    else:
        filesDir = []
        
    return filesDir


class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file  = forms.FileField(
        help_text='Upload user data',
        error_messages={
            'required': 'Required',
            'invalid': 'Invalid', 
            'missing': 'Missing', 
            'empty': 'Empty', 
            'max_length': 'Maximum length'
            }
    )


def upload_file(request, user):
    successful = True
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print >>sys.stderr,  "AAA", request.POST, request.FILES
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], user)
            return HttpResponseRedirect('/investigator/view_user/' + user)
        else:
            print >>sys.stderr,  "Invalid form in upload_file()"
            successful = False
    else:
        form = UploadFileForm()
    
    # adds 'user' to locals
    user = user
    
    return render_to_response('upload.html', locals(),
                              context_instance=RequestContext(request))


def handle_uploaded_file(uploaded_file, user):
    dir_path = os.path.join(USER_FILES, user)
    
    # create user's file directory if it does not exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
    file_path = os.path.join(dir_path, uploaded_file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

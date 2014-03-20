from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from Tangra.studies.models import *
from json_responses import *


def login(request):
    """Attempt to log the specified participant or investigator into the Tangra server. 
    
    POST arguments:
        username - The username of the participant or investigator.
        password - The password of the participant or investigator.
    
    Requires:
        request is a POST request.
    """
    try:        
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    # Correct password, and the user is marked "active"
                    auth.login(request, user)
                    return SuccessResponse()
                else:
                    # DISABLED ACCOUNT
                    return FailureResponse()
            else:
                # Invalid user?
                return FailureResponse()
        else:
            # Strange request. Send them back to the start
            return FailureResponse()
    except:
        return FailureResponse()


def logout(request):
    """Logs the user out of the Tangra server. Returns SUCCESS if the user is 
    not logged in to begin with or if the logout operation was successful."""
    
    try:
        logout(request)
        return SuccessResponse()
    except:
        return FailureResponse()


@login_required
def get_current_stage(request):
    """Return the index of the stage that the requesting user is currently on."""
    try:
        stage_number = get_current_stage_number(request.user)
        return JsonResponse(stage_number)
    except:
        return FailureResponse()


@login_required
def finish_current_stage(request):
    """assuming one user per study now... make things easy on ourselves for this
    project. generalize this after we've tested it on space fortress"""
    user = request.user
    current_stages = UserStage.objects.filter(user=request.user, status=1)
    if len(current_stages) == 0:
        # We should not be able to finish a nonexisting stage
        return FailureResponse()
    
    stage = current_stages[0]
    if stage.stage_times_completed >= stage.stage_times_total:
        # We should not be able to finish a nonexisting stage or finish a stage more times than specified
        return FailureResponse()
    
    stage.increase_stage_count()
    
    return SuccessResponse()
    


@login_required
def save_data(request):
    """Saves an arbitrary string of data for the requesting participant. The data will be 
    associated with the current stage the participant is on.
    
    An arbitrary number of data points can be saved for a given stage. These are returned 
    in a list when get_data or get_data_for_stage is called.
    
    POST arguments:
        data - The string of data to save
    """
    
    if request.method == 'POST':
        data_to_save = request.POST['data']
        code = "TXT"
        
        # TODO: Look at this line when redesigning the underlying database
        # TODO: address the issue of using a request.user in some places and a User object in others
        user = User.objects.get(username=request.user)
        study_id = UserStage.objects.filter(user=request.user, status=1)[0].stage.study.id
        stage = get_current_stage_number(request.user)
        
        try:
            Data.write(study_id, user, stage, datetime.datetime.now(), code, data_to_save)
            return SuccessResponse()
        except:
            return FailureResponse()
    else:
        return FailureResponse()


@login_required
def get_data(request):
    """Returns a list of all the data strings saved by the participant for their current stage."""
    
    # TODO: Look at this these when redesigning the underlying database
    # TODO: address the issue of using a request.user in some places and a User object in others
    user = User.objects.get(username=request.user)
    stage = get_current_stage_number(request.user)
    study = UserStage.objects.filter(user=request.user, status=1)[0].stage.study
    study_participant = StudyParticipant.objects.get(user=user, study=study)
    
    raw_user_data = Data.objects.filter(studyparticipant=study_participant)    
    
    return JsonResponse([entry.datum for entry in raw_user_data])
    



@login_required
def get_data_for_stage(request):
    """Returns a list of all the data strings saved by the participant for the specified stage
    
    POST Arguments:
        stage - The stage to query for previously submitted data.
    """
    
    stage = request.POST['stage']
    
    user = User.objects.get(username=request.user)
    stage_number = get_current_stage_number(request.user)
    
    asdfasdfASDFSADF ASDFasdfsafufkc
    
    study = get_study_object_for_stage_number(request.user)
    #study = UserStage.objects.filter(user=request.user, status=1)[0].stage.study
    
    study_participant = StudyParticipant.objects.get(user=user, study=study)
    
    raw_user_data = Data.objects.filter(studyparticipant=study_participant)    
    
    return JsonResponse([entry.datum for entry in raw_user_data])


@login_required
def save_data_with_key(request):
    """TODO: this lol"""
    return FailureResponse()


@login_required
def get_data_for_key(request):
    """TODO: this lol"""
    return FailureResponse()


@login_required
def get_data_for_stage_and_key(request):
    """TODO: this lol"""
    return FailureResponse()


@login_required
def upload_file(request):
    """TODO: this lol"""
    return FailureResponse()






###---------- old versions of the public api. revamping this to match the documentation now



@login_required
def get_user_data(request):
    user = request.user
    
    user_object = User.objects.get(username=user)
    sps = StudyParticipant.objects.filter(user=user_object)
    
    raw_user_data = []
    user_data = {}
    
    # for each study-participant entry
    # - ensure study's name has a placeholder in user_data dict
    for sp in sps:
        if sp.study.name not in user_data:
            user_data[sp.study.name] = {}
        raw_user_data.extend(Data.objects.filter(studyparticipant=sp))
    
    # go over raw data and organize it in user_data dict by study name
    for datum in raw_user_data:
        if datum.datum != "Session Completed":
            the_study = datum.studyparticipant.study.name
            user_data[the_study][int(datum.stage)] = datum.datum;
    
    # print >>sys.stderr,  user_data
    return HttpResponse(json.dumps(user_data), content_type="application/json")










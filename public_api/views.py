from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import os 

from Tangra import settings
from Tangra.studies.models import *
from json_responses import *
from tangra_error_codes import TangraErrorCodes


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
                    return SuccessResponse(None)
                else:
                    # DISABLED ACCOUNT
                    return FailureResponse(TangraErrorCodes.INVALID_CREDENTIALS)
            else:
                # Invalid user?
                return FailureResponse(TangraErrorCodes.INVALID_CREDENTIALS)
        else:
            # Strange request. Send them back to the start
            return FailureResponse(TangraErrorCodes.REQUIRES_POST)
    except:
        return FailureResponse(TangraErrorCodes.SERVER_ERROR)


def logout(request):
    """Logs the user out of the Tangra server. Returns SUCCESS if the user is 
    not logged in to begin with or if the logout operation was successful."""
    
    try:
        logout(request)
        return SuccessResponse(None)
    except:
        return FailureResponse(TangraErrorCodes.SERVER_ERROR)


@login_required
def get_current_stage(request):
    """Return the index of the stage that the requesting user is currently on."""
    try:
        stage_number = get_current_stage_number(request.user)
        if stage_number == None:
            return FailureResponse(TangraErrorCodes.INVALID_STAGE_REQUEST)
        else:
            return SuccessResponse(stage_number)
    except Exception, e:
        raise
        return FailureResponse(TangraErrorCodes.SERVER_ERROR)


@login_required
def finish_current_stage(request):
    """Marks the current stage as complete on the Tangra server.

    This assumes 1 study per user, which is not currently enforced. We need TODO
    this enforcement in the redesign of the core data model.
    """
    user = request.user
    current_stages = UserStage.objects.filter(user=request.user, status=1)
    if len(current_stages) == 0:
        # We should not be able to finish a nonexisting stage
        return FailureResponse(TangraErrorCodes.INVALID_STAGE_REQUEST)
    
    stage = current_stages[0]
    if stage.stage_times_completed >= stage.stage_times_total:
        # We should not be able to finish a nonexisting stage or finish a stage more times than specified
        return FailureResponse(TangraErrorCodes.INVALID_STAGE_REQUEST)
    
    stage.increase_stage_count()
    
    return SuccessResponse(None)
    


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
            return SuccessResponse(None)
        except:
            return FailureResponse(TangraErrorCodes.DATABASE_ERROR)
    else:
        return FailureResponse(TangraErrorCodes.REQUIRES_POST)



def get_data_for_user_and_stage_number(user, stage_number):
    """Returns a list of all data entries associated with the supplied user and stage number."""

    # TODO: Look at this these when redesigning the underlying database
    # TODO: address the issue of using a request.user in some places and a User object in others
    user_object = User.objects.get(username=user)
    study = UserStage.objects.filter(user=user, status=1)[0].stage.study
    study_participant = StudyParticipant.objects.get(user=user_object, study=study)
    
    raw_user_data = Data.objects.filter(studyparticipant=study_participant, stage=stage_number, key=None)    
    
    return [entry.datum for entry in raw_user_data]


@login_required
def get_data(request):
    """Returns a list of all the data strings saved by the participant for their current stage."""
    
    stage_number = get_current_stage_number(request.user)
    raw_data = get_data_for_user_and_stage_number(request.user, stage_number)

    return SuccessResponse(raw_data)


@login_required
def get_data_for_stage(request):
    """Returns a list of all the data strings saved by the participant for the specified stage
    
    POST Arguments:
        stage - The stage to query for previously submitted data.
    """
    
    stage_number = request.POST['stage']
    raw_data = get_data_for_user_and_stage_number(request.user, stage_number)

    return SuccessResponse(raw_data)



def get_data_object(username, stage_number, key=""):
    """Returns a Data object for the given user, stage and key. If no data object exists, this
    function returns None.

    Keyword Arguments:
        username - the username of the participant to retrieve data for.
        stage_number - The stage number associated with the requested data
        key - the key associated with the requested data
    """
    # TODO: address the issue of using a request.user in some places and a User object in others
    user = User.objects.get(username=username)
    study_id = UserStage.objects.filter(user=username, status=1)[0].stage.study.id
    study_participant = StudyParticipant.objects.get(user=user, study=study_id)

    try:
        data = Data.objects.get(studyparticipant=study_participant, stage=stage_number, key=key) 
        return data
    except Data.DoesNotExist:
        return None


@login_required
def save_data_with_key(request):
    """Saves an arbitrary string of data for the requesting participant. The data will be 
    associated with the current stage the participant is on and with the supplied key.
    
    Only one string can be saved for a given key and stage. If another call is made
    to this function on the same stage with the same key, then the old key will be 
    overwritten.
    
    POST arguments:
        data - The string of data to save.
        key - The key to associate with data.
    """
    if request.method == 'POST':
        data_to_save = request.POST['data']
        key = request.POST['key']
        
        data = get_data_object(request.user, get_current_stage_number(request.user), key)
        if data == None:
            user = User.objects.get(username=request.user)
            study_id = UserStage.objects.filter(user=request.user, status=1)[0].stage.study.id
            study_participant = StudyParticipant.objects.get(user=user, study=study_id)
            data = Data(studyparticipant=study_participant, stage=get_current_stage_number(request.user), key=key)
        
        data.code = "TXT"
        data.timestamp = datetime.datetime.now()
        data.datum = data_to_save

        data.save()

        return SuccessResponse()
        #except:
        #    return FailureResponse()
    else:
        return FailureResponse()


@login_required
def get_data_for_key(request):
    """Returns the string saved for the supplied key in the participant's current stage, or 
    a FailureResponse if no data was saved for the supplied key.

    TODO: finish documentation omg
    """
    if request.method == 'POST':
        key = request.POST['key']
        
        data = get_data_object(request.user, get_current_stage_number(request.user), key)
        if data == None:
            return FailureResponse()
        else:
            return JsonResponse(data.datum)
        #except:
        #    return FailureResponse()
    else:
        return FailureResponse()


@login_required
def get_data_for_stage_and_key(request):
    """Returns the string saved for the supplied key in the participant's current stage, or 
    a FailureResponse if no data was saved for the supplied key.

    TODO: finish documentation omg
    """

    if request.method == 'POST':
        key = request.POST['key']
        stage_number = request.POST['stage']

        data = get_data_object(request.user, stage_number, key)
        if data == None:
            return FailureResponse()
        else:
            return JsonResponse(data.datum)
        #except:
        #    return FailureResponse()
    else:
        return FailureResponse()
    return FailureResponse()


def handle_uploaded_file(uploaded_file, user):
    dir_path = os.path.join(settings.USER_FILES, user)
    
    # create user's file directory if it does not exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    file_path = os.path.join(dir_path, uploaded_file.name)

    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)


@login_required
def upload_file(request):
    """Upload a file to the participant's data directory.

    POST Arguments:

    """
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['file'], request.user.username)
        return SuccessResponse()
    else:
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










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



def get_data_for_user_and_stage_number(user, stage_number):
    """Returns a list of all data entries associated with the supplied user and stage number."""

    # TODO: Look at this these when redesigning the underlying database
    # TODO: address the issue of using a request.user in some places and a User object in others
    user_object = User.objects.get(username=user)
    study = UserStage.objects.filter(user=user, status=1)[0].stage.study
    study_participant = StudyParticipant.objects.get(user=user_object, study=study)
    
    raw_user_data = Data.objects.filter(studyparticipant=study_participant, stage=stage_number)    
    
    return [entry.datum for entry in raw_user_data]


@login_required
def get_data(request):
    """Returns a list of all the data strings saved by the participant for their current stage."""
    
    stage_number = get_current_stage_number(request.user)
    raw_data = get_data_for_user_and_stage_number(request.user, stage_number)

    return JsonResponse(raw_data)


@login_required
def get_data_for_stage(request):
    """Returns a list of all the data strings saved by the participant for the specified stage
    
    POST Arguments:
        stage - The stage to query for previously submitted data.
    """
    
    stage_number = request.POST['stage']
    raw_data = get_data_for_user_and_stage_number(request.user, stage_number)

    return JsonResponse(raw_data)



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
        
        # TODO: Look at this line when redesigning the underlying database
        # TODO: address the issue of using a request.user in some places and a User object in others
        user = User.objects.get(username=request.user)
        study_id = UserStage.objects.filter(user=request.user, status=1)[0].stage.study.id
        stage_number = get_current_stage_number(request.user)
        study_participant = StudyParticipant.objects.get(user=user, study=study_id)

        try:
            data = Data.objects.get(studyparticipant=study_participant, stage=stage_number, key=key) 
        except Data.DoesNotExist:
            data = Data(studyparticipant=study_participant, stage=stage_number, key=key)
        
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
    """

    if request.method == 'POST':
        key = request.POST['key']
        
        # TODO: Look at this line when redesigning the underlying database
        # TODO: address the issue of using a request.user in some places and a User object in others
        user = User.objects.get(username=request.user)
        study_id = UserStage.objects.filter(user=request.user, status=1)[0].stage.study.id
        stage_number = get_current_stage_number(request.user)
        study_participant = StudyParticipant.objects.get(user=user, study=study_id)

        try:
            data = Data.objects.get(studyparticipant=study_participant, stage=stage_number, key=key)
            return JsonResponse(data.datum)
        except Data.DoesNotExist:
            return FailureResponse() # TODO: really need to make the return value more powerful... blargh
        #except:
        #    return FailureResponse()
    else:
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










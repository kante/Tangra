from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponse

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from studies.models import *
from studies.views import finish_session

def login(request):
    """Try to log in."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                return HttpResponse("Logged in successfully!")    
            else:
                # DISABLED ACCOUNT
                return HttpResponse("That was a disabled account!")    
        else:
            # Invalid user?
            return HttpResponse("Invalid user!")    
    else:
        # Strange request. Send them back to the start
        return HttpResponse("Strange request... not POST!?")    



@login_required
def testing(request):
    #send: studyid, request.user, time, data
    return HttpResponse("bwwaaahahaha! awww yeah!")




@login_required
def get_current_stage_info(request):
    user = request.user
    current_stages = UserStage.objects.filter(user=request.user, status=1)

    # assuming one user per study now... make things easy on ourselves for this
    # project. generalize this after we've tested it on space fortress
    stage = current_stages[0]
    print "ASDF", stage
    return HttpResponse("stage_name:"+stage.stage.name+
        ",stage_times_completed:"+str(stage.stage_times_completed))




@login_required
def fsess(request):
    finish_session(request)

    return HttpResponse("OK")

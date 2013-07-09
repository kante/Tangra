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
    old_stages = UserStage.objects.filter(user=request.user, status=0)
        
    stage_num=1
    for stage in old_stages:
        stage_num = stage_num + stage.stage_times_total
        
        
    # assuming one user per study now... make things easy on ourselves for this
    # project. generalize this after we've tested it on space fortress
    stage = current_stages[0]
    stage_num = stage_num + stage.stage_times_completed
    return HttpResponse("stage_name:" + stage.stage.name +
                        ",current_stage_num:"+str(stage_num) +
                        ",stage_custom_data:" + str(stage.custom_data))


@login_required
def fsess(request):
    # assuming one user per study now... make things easy on ourselves for this
    # project. generalize this after we've tested it on space fortress    user = request.user
    current_stages = UserStage.objects.filter(user=request.user, status=1)
    stage = current_stages[0]
    stage.increase_stage_count()
    
    return HttpResponse("OK")

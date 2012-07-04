from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponse

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



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









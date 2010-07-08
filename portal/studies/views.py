from django.shortcuts import render_to_response
from django.template import RequestContext
import hashlib

from django.http import HttpResponseRedirect
from models import *
from forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#from blank import Blank



############### Study
@login_required
def show_many_studies(request):
	if StudyUser.objects.count > 0:
		#studies = [x.study for x in StudyUser.objects.filter(user=request.user)]
		study_users = StudyUser.objects.filter(user=request.user)
	else:
		study_users = []
		
	return render_to_response('show_many_studies.html', locals(), context_instance=RequestContext(request))

@login_required
def show_one_study(request,study_id):
	study = Study.objects.get(id=study_id)
	study_user = study.getstudyuser(request.user)
	stages = study_user.stages
	return render_to_response('show_one_study.html',locals(), context_instance=RequestContext(request))
	
@login_required
def show_users_in_study(request,study_id):
	users = Study.objects.get(id=study_id).users()
	return render_to_response('show_users.html', locals(), context_instance=RequestContext(request))

@login_required
def create_one_study(request):
	if request.method == 'POST':
		form = NewStudyForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data

			s = Study.objects.create(
				name=cd['name'],
				start_date=cd['start_date'],
				end_date=cd['end_date'],
				started=cd['started'],
				description=cd['description'])
			s.create_study_user(request.user)
			return HttpResponseRedirect('/study/'+str(s.id))
	else:
		#study = Blank()
		form = NewStudyForm()
	return render_to_response('new_study.html', locals(), context_instance=RequestContext(request))
		
@login_required		
def edit_one_study(request,study_id):
	"""docstring for edit_one_study"""
	if request.method == 'POST':
		pass #update
	else: #render the form
		study = Study.objects.get(id=study_id)
		form = NewStudyForm(instance=study)
		return render_to_response('edit_study.html',locals(), context_instance=RequestContext(request))

@login_required
def remove_one_study(request,study_id):
	"""docstring for remoe_one_study"""
	s = Study.objects.get(id=study_id)
	StudyUser.objects.filter(study=s).delete()
	
	s.delete()
	return HttpResponseRedirect('/study/')
	
@login_required
def add_participant_to_study(request,study_id):
	"""docstring for add_participant_to_study"""
	if request.method == 'POST':
		newuser = False
		form = AddParticipantForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			study = Study.objects.get(id=study_id)
			query = cd['email']
			user = User.objects.filter(email=query)
			
			if len(user) == 0:
				newuser = True
				pwd = hashlib.new('ripemd160')
				pwd.update(cd['email'])
				pwd = pwd.hexdigest()[:10]
				user = User.objects.create_user(username=cd['email'],email=cd['email'],password=pwd)
				user.message_set.create(message=pwd)
			else:
				user = user[0]
			study.create_study_user(user)
			return HttpResponseRedirect('/study/added_to_study/'+ str(user.id)+"/"+str(study.id))
		else:
			return render_to_response('add_participant_to_study.html',locals(), context_instance=RequestContext(request))
	else: #render the form
		study = Study.objects.get(id=study_id)
		form = AddParticipantForm()
		return render_to_response('add_participant_to_study.html',locals(), context_instance=RequestContext(request))

@login_required
def added_to_study(request, study_id, user_id):
	"""docstring for added_to_study"""
	useradded = User.objects.get(id=user_id)
	study = Study.objects.get(id=study_id)

	message = useradded.get_and_delete_messages()
	if len(message) == 0 :
		message = None
	else:
		message = message[0]
	new = not (message is None)
	return render_to_response('added_to_study.html',locals(), context_instance=RequestContext(request))

############### StudyUser

def invite_user(request,study_id):
	pass
	
def remove_user(request,study_id,user_id):
	pass



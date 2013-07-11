from django.contrib.auth.models import User


from studies.models import Study, Group, Stage, StageGroup, StudyParticipant, UserStage
from users.models import UserRoles
import datetime



def add_study_to_db(study_settings):
    """
    study_settings - A StudySettings object to create database entries for.
    """
    study = create_studies(study_settings)
    create_participants(study_settings, study)
    create_stages(study_settings)
    create_groups(study_settings)
    create_investigators(study_settings, study)


def create_participants(study_settings, study):
    """
        Create user entries in the database for the supplied study_settings
        
        This will override any existing users password with the one that is
        supplied in settings.xml
    """
    
    for username in study_settings.participants:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username)
        
        user.set_password(study_settings.passwords[username])
        user.save()
        
        # now update the user profile (it should be created after the save)
        profile = user.get_profile()
        profile.user_role = UserRoles.PARTICIPANT
        profile.save()
        
        # add the investigators to the study
        study.participants.add(user)


def create_investigators(study_settings, study):
    """
        Create user entries in the database for the supplied study_settings

        This will override any existing users password with the one that is
        supplied in settings.xml
    """

    for username in study_settings.investigators.keys():
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username)

        user.set_password(study_settings.investigators[username])
        user.save()

        # now update the user profile (it should be created after the save)
        profile = user.get_profile()
        profile.user_role = UserRoles.INVESTIGATOR
        profile.save()
        
        # add the investigators to the study
        study.investigators.add(user)



def create_studies(study_settings):
    """
        Create Study entries in the database for the supplied study_settings
    """
    try:
        study = Study.objects.get(name=study_settings.name)
    except Study.DoesNotExist:
        study = Study(name=study_settings.name)
    
    study.stub = study_settings.name_stub
    study.description = study_settings.description
    #study.start_date = Date
    #study.end_date = Date
    study.started = True
    study.consent = study_settings.informed_consent
    study.instructions = study_settings.instructions
    study.eligibility = study_settings.eligibility
    study.reward = study_settings.reward
    study.task_session_dur = 1
    study.assess_blocks = 1
    study.assess_trials = 1
    
    study.save()
    
    return study
  

def create_group(study, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        group = Group(name=group_name)

    group.study = study
    group.save()
    
    return group


def create_groups(study_settings):
    """
        Create Group entries in the database for study_settings
        
        TODO: Warn user if a group already exists under another study
    """

    # create_studies was called before this so we should have the study
    # object in the database
    study = Study.objects.get(name=study_settings.name)
    for group_name in study_settings.groups.keys():
        users = study_settings.groups[group_name]['users']
        stages = study_settings.groups[group_name]['stages']
        times = study_settings.groups[group_name]['times']
        custom_data = study_settings.groups[group_name]['custom_data']

        group = create_group(study, group_name)
        
        # specify the order that the stages appear for this group
        stage_index = 0
        # for stage_name in stages:
        for i in range(len(stages)):
            stage_name = stages[i]
            
            stage_times_total = times[i]
            if stage_times_total == '':
                stage_times_total = 1
            else:
                stage_times_total = int(stage_times_total)
            stage_times_completed = 0
                
            stage = Stage.objects.get(name=stage_name, study=study)
            try:
                stage_group = StageGroup.objects.get(group=group, stage=stage, order=stage_index)
            except StageGroup.DoesNotExist:
                stage_group = StageGroup(group=group, stage=stage, order=stage_index, stage_times_total=stage_times_total, \
                                         custom_data=custom_data[i])
            stage_group.save()
            
            
            # add study participants for the group
            for username in users:
                user = User.objects.get(username=username)
                try:
                    study_participant = StudyParticipant.objects.get(study=study, user=user, group=group)
                except StudyParticipant.DoesNotExist:
                    study_participant = StudyParticipant(study=study, user=user, group=group)
                study_participant.save()
                
                # add a UserStage for each user/stage pair
                try:
                    user_stage = UserStage.objects.get(stage=stage, user=user, order=stage_index, study=study)
                except UserStage.DoesNotExist:
                    user_stage = UserStage(stage=stage, user=user, order=stage_index, \
                                            study=study, stage_times_completed=0, stage_times_total=stage_times_total, \
                                            custom_data=custom_data[i])
                
                # set all status to incomplete
                user_stage.status = 1 if stage_index == 0 else 2
                user_stage.sessions_completed = 0
                user_stage.start_date = datetime.datetime.now()
                user_stage.save()
                
                
            stage_index = stage_index + 1
            


def create_stages(study_settings):
    """
    Create Stage entries in the database study_settings
    """

    study = Study.objects.get(name=study_settings.name)
    
    for (stage_name, description) in zip(study_settings.stages, study_settings.stage_descriptions):
        try:
            stage = Stage.objects.get(study=study, name=stage_name)
        except Stage.DoesNotExist:
            stage = Stage(study=study, name=stage_name)
        stage.stub = stage_name[0:3]
        stage.sessions = 1
        stage.deadline = 7
        
        stage.url = "/user_studies/{0}/{1}".format(study.name, stage.name)
         
        stage.description = description
        stage.instructions = description
        
        stage.save()
    





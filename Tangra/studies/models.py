from django.db import models
from django.contrib.auth.models import User
import datetime
from operator import attrgetter


def get_current_stage_object(user):
    """Returns the current Stage object for the supplied user. Note that we are 
    assuming only one study per user.
    """
    current_stages = UserStage.objects.filter(user=user, status=1)
    return current_stages[0]


def get_current_stage_number(user):
    """Return the current stage number for the supplied user. Note that for stages
    with multiple completions or infinite stages, each time the stage is completed 
    is counted as a separate stage.
    
    Keyword Arguments:
        user - The Tangra participant to find the current stage for.
    """
    current_stages = UserStage.objects.filter(user=user, status=1)
    old_stages = UserStage.objects.filter(user=user, status=0)
    
    stage_number=1
    for stage in old_stages:
        stage_number = stage_number + stage.stage_times_total

    # assuming one user per study now... TODO: enforce this when revamping old
    # model/database structure
    stage = current_stages[0]
    stage_number = stage_number + stage.stage_times_completed
    
    return stage_number


class Study(models.Model):
    name = models.CharField('Study Name', max_length=300)
    stub = models.CharField('Study Stub', max_length=3)
    description = models.CharField('Description', max_length=5000)
    start_date = models.DateField('Starting Date', blank=True, null=True)
    end_date = models.DateField('End Date', blank=True, null=True)
    started =  models.BooleanField('Started', default=False)

    consent = models.CharField('Informed Consent Form', max_length=5000)
    instructions = models.CharField('Study Instructions', max_length=5000)
    eligibility = models.CharField('Eligibility Criteria', max_length=5000)
    reward = models.CharField('Compensation and Reward', max_length=5000)
    
    # lists of investigators and participants associated with this study
    investigators = models.ManyToManyField(User, related_name="investigators")
    participants = models.ManyToManyField(User, related_name="participants")
    
    #added to customize durations
    task_session_dur = models.IntegerField("Session Duration (minutes)")
    assess_blocks = models.IntegerField("Number of assessment blocks")
    assess_trials = models.IntegerField("Number of trials per block")
    
    
    def save(self, *args,**kwargs):    
        #create timestamps, keep track of user
        super(Study, self).save(*args, **kwargs) 
    
    
    def get_study_participant(self, user):
        s = StudyParticipant.objects.get(study=self, user=user)
        return s
    
    
    def __unicode__(self):
        return u'%s' % (self.name)


class Group(models.Model):
    name = models.CharField('Group Name', max_length=300)
    study = models.ForeignKey(Study)
    
    def __unicode__(self):
        return u'%s - %s' % (self.study, self.name)     
    
    def stages(self):
        return [x.stage for x in StageGroup.objects.filter(group=self).order_by('order')]


class StudyParticipant(models.Model):
    study = models.ForeignKey(Study)
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    
    def participant_stages(self):
        return UserStage.objects.filter(user=self.user).order_by('order')
    
    def number_of_stages(self):
        return self.participant_stages().count()
    
    def save(self):
        #create timestamps, keep track of user modifying, etc.
        super(StudyParticipant,self).save()
    
    def __unicode__(self):
        return u'%s - %s (Participant)' % (self.user,self.study)        
    
    def log(self):
        return u'%s,%s' % (self.user.username,self.study.stub)


class Stage(models.Model):
    name = models.CharField('Stage Name', max_length=300)
    stub = models.CharField('Stage Stub', max_length=3)
    study = models.ForeignKey(Study)
    sessions = models.IntegerField('Number of sessions')
    deadline = models.IntegerField('Time to finish session (in days)')
    url = models.CharField('Stage URL', max_length=300)
    description = models.CharField('Stage Description', max_length=5000)
    instructions = models.CharField('Stage Instructions', max_length=5000)


    def __unicode__(self):
        return unicode("%s (%s)" % (self.name, self.study.stub))       
    
    def display(self):
        return unicode(self.name)
    
    def avg(self):
        """docstring for avg"""
        stagegroups = StageGroup.objects.filter(stage=self)
        total = 0
        for x in stagegroups:
            total += x.order
        return total/len(stagegroups)
    
    def number_of_users(self):
        return self.users().count()
    
    def users(self):
        return UserStage.objects.filter(stage=self, status=1).order_by('user')


class StageGroup(models.Model):
    group = models.ForeignKey(Group)
    stage = models.ForeignKey(Stage)
    order = models.IntegerField()
    custom_data = models.CharField('Custom Data', max_length=5000)
    stage_times_total = models.IntegerField('Total times for stage')
    
    @classmethod
    def stages_in_group(cls, group):
        """docstring for stages_in_group"""
        return [x.stage for x in StageGroup.objects.filter(group=group).order_by('order')]
    
    def __unicode__(self):
        return u'%s - %s (%s)' % (self.stage, self.group, self.order)


class Data(models.Model):
    """A data object"""
    
    studyparticipant = models.ForeignKey(StudyParticipant)
    stage = models.IntegerField('Stage')
    timestamp = models.DateTimeField('Timestamp')
    datum = models.TextField('Datum')
    code = models.CharField(max_length=3)
    
    @classmethod
    def write(cls, studyid, user, stage, time, code, data):
        d = Data()
        d.studyparticipant = Study.objects.get(id=studyid).get_study_participant(user) 
        d.stage = stage
        d.timestamp = time
        d.datum = data
        d.code = code        
        d.save()
    
    def __unicode__(self):
        return u'%s,%s,%s,%s,%s' % (self.studyparticipant.log(), self.stage, self.format_timestamp(), self.code, self.datum)
    
    def data(self):
        return u'%s,%s,%s,%s,%s' % (self.studyparticipant.log(), self.stage, self.format_timestamp(), self.code, self.datum)
        
    def format_timestamp(self):
        t = self.timestamp
        return u'%s,%s,%s,%s,%s,%s,%s' % (t.year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond/1000)
    
    
class UserStage(models.Model):
    user = models.ForeignKey(User)
    stage = models.ForeignKey(Stage)
    order = models.IntegerField('Order', editable=False)
    CHOICES = ((0, 'Completed'),(1, 'Active'),(2, 'Future'))
    status = models.IntegerField('Status', max_length=1, choices=CHOICES)
    start_date = models.DateTimeField('Start date', blank=True, null=True)
    end_date = models.DateTimeField('End date', blank=True, null=True)
    sessions_completed = models.IntegerField('Sessions completed')
    last_session_completed = models.DateTimeField('Last session completed', blank=True, null=True)
    curr_session_started = models.DateTimeField('Current session started', blank=True, null=True)
    study = models.ForeignKey(Study)
    
    # some of this is copied over from StageGroup... do we need this?
    stage_times_completed = models.IntegerField('Times stage completed')
    custom_data = models.CharField('Custom Data', max_length=5000)
    stage_times_total = models.IntegerField('Total times for stage')
    
    
    def __unicode__(self):
        return u'%s - %s (%s)' % (self.user, self.stage, self.order)
    
    def save(self, *args,**kwargs):
        super(UserStage, self).save(*args, **kwargs)
        #self.set_order()
            
    def group(self):
        return StudyParticipant.objects.get(user=self.user).group       

    def infinite_session_completed(self):
        self.session_completed(self)

    def session_completed(self):
        stage_number = get_current_stage_number(self.user)
        self.last_session_completed = datetime.datetime.now()
        Data.write(self.study.id, self.user, stage_number, self.last_session_completed, "SSC", "Stage Completed")
        
        self.sessions_completed += 1
        if self.sessions_completed == self.stage.sessions:
            #this stage is finished
            self.status = 0
            self.end_date = datetime.datetime.now()
            #find next stage
            try:
                next = UserStage.objects.get(user=self.user, study=self.study, order=self.order+1)
                next.status = 1
                next.start_date = datetime.datetime.now()
                next.last_session_completed = next.start_date
                next.save()
            except UserStage.DoesNotExist:
                #end of study
                pass
                
        self.save()
    
    def increase_stage_count(self):
        self.stage_times_completed += 1
        self.save()
        if self.stage_times_completed == self.stage_times_total:
            self.session_completed()

    def stage_completed(self):
        self.sessions_completed = self.stage.sessions
        self.last_session_completed = datetime.datetime.now()
        Data.write(self.study.id, self.user, self.last_session_completed, "session completed", "ssc")
        self.status = 0
        self.end_date = datetime.datetime.now()
        #find next stage
        next = UserStage.objects.get(user=self.user, order=self.order+1)
        if len(next) == 0:
            #end of study
            pass
        else:
            next.status = 1
            next.start_date = datetime.datetime.now()
            next.save()
        self.save()       

    def start_stage(self):
        self.curr_session_started = datetime.datetime.now()
        self.save()
        
    def set_order(self):
        self.order = StageGroup.objects.get(group=self.group(), user=self.user).order
        
    def users_in_stage(self, stage_object):
        return UserStage.objects.filter(stage=stage_object, status=1)

    def number_users_in_stage(self, stage_object):
        """docstring for number_users_in_stage"""
        return len(self.users_in_stage(stage_object))

    def nextdeadline(self):
        ahead = datetime.timedelta(days=self.stage.deadline)
        return self.start_date + ahead
        
    def overdue(self):
        if datetime.datetime.now() > self.nextdeadline():
            return True
        return False


    
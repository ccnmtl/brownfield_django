import datetime
from django.db import models
from django.contrib.auth.models import User

PROFILE_CHOICES = (
    ('TE', 'Teacher'),
    ('ST', 'Student'),
)


'''
Old Tables:
             "Visit",
             "User",
             "VisitIdentity",
             "Permission",
             "Group",
             "Document",
             "Course",
             "Team",
             "Student",
             "History",
             "PerformedTest",
             "Information",
'''



class Course(models.Model):
    '''Course'''
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, default='')
    startingBudget = models.PositiveIntegerField(default=60000)
    enableNarrative = models.BooleanField(default=True)
    message = models.TextField(max_length=255)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, related_name="created_by", null=True, default=None, blank=True)
    initial_budget = models.PositiveIntegerField(default=65000)

    def __unicode__(self):
        return self.name

    def get_students(self):
        participants = UserProfile.objects.filter(course=self)
        # need to exclude teacher
        return participants


class Document(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    visible = models.BooleanField(default=False)
    # in old application content is href not sure if it should be but...


class Team(models.Model):
    '''Team: A team will have one login/username
    All accounting/history/actions is by team.
    SINCE USER PROFILE IS A TEAM DO WE NEED TO
    MAKE THIS HAVE A RELATION TO USER< OR JUST USE
    THIS TO STORE USER TYPE TEAM DATA?
    '''
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course)
    team_entity = models.OneToOneField(User)
    signed_contract = models.BooleanField(default=False)
    budget = models.PositiveIntegerField(default=65000)

    class Meta:
        '''We don't want teams with the same name in a course'''
        ordering = ['name']
        unique_together = ['name', 'course']

    def __unicode__(self):
        return self.name
    
    def get_members(self):
        try:
            members = self.userprofile_set.all()
            return members
        except:
            return None
        
    def get_signed_contract(self):
        return self.signed_contract
    
    def get_course(self):
        return self.course


class UserProfile(models.Model):
    '''UserProfile adds extra information to a user,
    and associates the user with a team, course,
    and course progress.'''
    user = models.OneToOneField(User, related_name="profile")
    # interactive = models.ForeignKey(Interactive, null=True, blank=True)
    profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)
    course = models.ForeignKey(Course, null=True, default=None, blank=True)
    team = models.ForeignKey(Team, null=True, default=None, blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ["user"]

    def display_name(self):
        return self.user.username

    def is_student(self):
        return self.profile_type == 'ST'

    def is_teacher(self):
        return self.profile_type == 'TE'

    def role(self):
        if self.is_student():
            return "student"
        elif self.is_teacher():
            return "faculty"



    

class History(models.Model):
    team = models.ForeignKey(Team)
    date = models.DateTimeField(default=datetime.datetime.now)
    description = models.CharField(max_length=255)
    cost = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s - %s' % (self.description, self.team)


class PerformedTest(models.Model):
    X = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    testNumber = models.IntegerField(default=0)
    paramString = models.CharField(max_length=255)

    def __unicode__(self):
        return self.paramString


class Visit(models.Model):
    pass 
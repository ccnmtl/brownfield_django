from django.db import models
from django.contrib.auth.models import User
from brownfield_django.interactive.models import Interactive

PROFILE_CHOICES = (
    ('TE', 'Teacher'),
    ('ST', 'Student'),
    ('TM', 'Team'),
)

DOCUMENT_TYPE = (
    ('SLC', 'Self-Lume Catalog'),
    ('SLB', 'Self-Lume Brochure'),
    ('SLP', 'Self-Lume Property Map'),
    ('COC', 'Copy of Contract'),
    ('VSR', 'Visual Reconnaissance'),
)

'''Why does old application have so many database tables? Definately
seems to be overkill
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

class UserProfile(models.Model):
    '''UserProfile adds extra information to a user,
    and associates the user with a team, course,
    and course progress.'''
    user = models.OneToOneField(User, related_name="profile")
    interactive = models.ForeignKey(Interactive, null=True, blank=True)
    profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)
    budget = models.PositiveIntegerField(default=60000)

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
    
    def is_team(self):
        return self.profile_type == 'TM'

    def role(self):
        if self.is_student():
            return "student"
        elif self.is_teacher():
            return "faculty"
        elif self.is_team():
            return "team"


class Course(models.Model):
    '''Course'''
    name = models.CharField(max_length=255)
    startingBudget = models.PositiveIntegerField(default=60000)
    enableNarrative = models.BooleanField(default=True)
    message = models.TextField(max_length=255)
    active = models.BooleanField(default=True)
    participant = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return self.name


class Document(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    document_type = models.CharField(max_length=3, choices=DOCUMENT_TYPE, default=None, blank=True)
    # in old application content is href not sure if it should be but...


class Team(models.Model):
    '''Team: A team will have one login/username
    All accounting/history/actions is by team.
    SINCE USER PROFILE IS A TEAM DO WE NEED TO
    MAKE THIS HAVE A RELATION TO USER< OR JUST USE
    THIS TO STORE USER TYPE TEAM DATA?
    '''
    class Meta:
        '''We don't want teams with the same name in a course'''
        ordering = ['name']
        unique_together = ['name', 'course']

    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course)
    signed_contract = models.BooleanField(default=False)

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
    



class PerformedTest(models.Model):
    X = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    testDetails = models.CharField(max_length=255)
    paramString = models.CharField(max_length=255)


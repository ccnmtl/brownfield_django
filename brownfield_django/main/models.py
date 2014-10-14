import datetime
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


PROFILE_CHOICES = (
    ('AD', 'Administrator'),
    ('TE', 'Teacher'),
    ('TM', 'Team'),
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
    '''
    Course Model - I added an archive field to indicate if a
    course should be excluded from the Dashboard, without necessarily
    deleting all of the data in case it is needed at a later time.

    Added creator field but since only admins will be allowed to view
    everyone's courses, and since they may create a course on a professor's
    behalf, I changed it to be a professor/instructor field.
    '''
    name = models.CharField(max_length=255)
    startingBudget = models.PositiveIntegerField(default=60000)
    enableNarrative = models.BooleanField(default=True)
    message = models.TextField(max_length=255, default='')
    active = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)
    professor = models.ForeignKey(User, related_name="taught_by", null=True,
                                  default=None, blank=True)

    def __unicode__(self):
        return self.name

    def get_students(self):
        return self.userprofile_set.filter(profile_type='ST')

    def get_students_without_team(self):
        return self.userprofile_set.filter(profile_type='ST', in_team=False)

    def get_teams(self):
        return self.userprofile_set.filter(profile_type='TM')

    def get_team_members(self, name):
        return self.userprofile_set.filter(profile_type='ST', team_name=name)

    def get_documents(self):
        documents = Document.objects.filter(course=self)
        return documents

    def get_course_form(self):
        form = CourseForm()
        return form


class CourseForm(ModelForm):
    class Meta:
        model = Course


class Document(models.Model):
    course = models.ForeignKey(Course, null=True,
                               default=None, blank=True)
    name = models.CharField(max_length=255, default='')
    link = models.CharField(max_length=255, default='')
    visible = models.BooleanField(default=False)


class UserProfile(models.Model):
    '''UserProfile adds extra information to a user,
    and associates the user with a team, course,
    and course progress.'''
    user = models.OneToOneField(User, related_name="profile")
    profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)
    course = models.ForeignKey(Course, null=True, default=None, blank=True)
    '''
    Even though these are only applicable to a Team
    I'm sticking them here.
    '''
    signed_contract = models.BooleanField(default=False)
    budget = models.PositiveIntegerField(default=65000)
    '''
    Adding extra fields here to keep track of teams and students.
    Fields should act as tags on Profiles of student type.
    '''
    in_team = models.BooleanField(default=False)
    team_name = models.CharField(max_length=255, default="", blank=True)
    '''
    We need a plain text copy of the password to email the students
    '''
    team_passwd = models.CharField(max_length=255, default="", blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ["user"]

    def display_name(self):
        return self.user.username

    def is_student(self):
        return self.profile_type == 'ST'

    def is_team(self):
        return self.profile_type == 'TM'

    def is_teacher(self):
        return self.profile_type == 'TE'

    def is_admin(self):
        return self.profile_type == 'AD'

    def role(self):
        if self.is_student():
            return "student"
        elif self.is_team():
            return "team"
        elif self.is_teacher():
            return "faculty"
        elif self.is_admin():
            return "administrator"


class History(models.Model):
    team = models.ForeignKey(UserProfile)
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

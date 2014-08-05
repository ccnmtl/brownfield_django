from django.db import models
from django.contrib.auth.models import User


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
    content = models.CharField(max_length=255)
    # in old application content is href not sure if it should be but...


class Team(models.Model):
    '''Team: A team will have one login/username
    All accounting/history/actions is by team.'''
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course)
    signed_contract = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class PerformedTest(models.Model):
    X = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    testDetails = models.CharField(max_length=255)
    paramString = models.CharField(max_length=255)


class UserProfile(models.Model):
    '''UserProfile adds exta information to a user,
    and associates the user with a team, course,
    and course progress.'''
    user = models.OneToOneField(User, related_name="profile")
    profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)

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

    def joined_groups(self):
        '''Groups this user has joined'''
        return self.course_set.all()


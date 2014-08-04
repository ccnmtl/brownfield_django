from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    '''Course'''
    name = models.CharField(max_length=255)
    startingBudget = models.PositiveIntegerField(default=60000)
    enableNarrative = models.BooleanField(default=True)
    # original default is none
    message = models.TextField(max_length=255)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Team(models.Model):
    '''Team: A team will have one login/username
    All accounting/history/actions is by team.'''
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course)
    signed_contract = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Student(models.Model):
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)


class PerformedTest(models.Model):
    X = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    testDetails = models.CharField(max_length=255)
    paramString = models.CharField(max_length=255)

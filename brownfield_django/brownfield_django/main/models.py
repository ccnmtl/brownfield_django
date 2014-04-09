from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
from pagetree.models import Section, Hierarchy, UserLocation, UserPageVisit


class Course(models.Model):
    '''Course'''
    name = models.CharField(max_length=255)
    startingBudget = models.PositiveIntegerField(default=60000)
    enableNarrative = models.BooleanField(default=True)
    #users = models.ManyToManyField(User)
    #course can have many students --> student class will have the foriegn key to course
    message = models.CharField(max_length=255) # original default is none
    #documents = models.ManyToMany(Document)
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


# class UserProfile(models.Model):
#     user = models.ForeignKey(User, related_name="application_user")
#     profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)
#     country = models.ForeignKey(Country, null=True, blank=True)
#     school = models.ForeignKey(School, null=True, default=None)
#     course = models.ManyToManyField(Course, null=True, blank=True)
#
#     def __unicode__(self):
#         return self.user.username
#
#     class Meta:
#         ordering = ["user"]
#
#     def get_has_visited(self, section):
#         return section.get_uservisit(self.user) is not None
#
#     def set_has_visited(self, sections):
#         for sect in sections:
#             sect.user_pagevisit(self.user, "complete")
#             sect.user_visit(self.user)
#
#     def last_location(self, hierarchy_name=None):
#         if hierarchy_name is None:
#             hierarchy_name = self.role()
#         hierarchy = Hierarchy.get_hierarchy(hierarchy_name)
#         try:
#             UserLocation.objects.get(user=self.user,
#                                      hierarchy=hierarchy)
#             return hierarchy.get_user_section(self.user)
#         except UserLocation.DoesNotExist:
#             return hierarchy.get_first_leaf(hierarchy.get_root())
#
#     def percent_complete(self):
#         hierarchy = Hierarchy.get_hierarchy(self.role())
#         visits = UserPageVisit.objects.filter(section__hierarchy=hierarchy)
#         sections = Section.objects.filter(hierarchy=hierarchy)
#         if len(sections) > 0:
#             return int(len(visits) / float(len(sections)) * 100)
#         else:
#             return 0
#
#     def display_name(self):
#         return self.user.username
#
#     def is_student(self):
#         return self.profile_type == 'ST'
#
#     def is_teacher(self):
#         return self.profile_type == 'TE'
#
#     def role(self):
#         if self.is_student():
#             return "student"
#         elif self.is_teacher():
#             return "teacher"

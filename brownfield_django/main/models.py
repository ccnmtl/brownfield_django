import datetime
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from brownfield_django.main.document_links import NAME_1, \
    LINK_1, NAME_2, LINK_2, NAME_3, LINK_3, NAME_4, LINK_4, \
    NAME_5, LINK_5, NAME_6, LINK_6, NAME_7, LINK_7, NAME_8, LINK_8


PROFILE_CHOICES = (
    ('AD', 'Administrator'),
    ('TE', 'Teacher'),
    ('ST', 'Student'),
)


class Course(models.Model):
    '''
    Course Model
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

    def save(self, *args, **kwargs):
        if self.pk is None:
            d1 = Document.objects.create(course=self, name=NAME_1,
                                         link=LINK_1)
            d2 = Document.objects.create(course=self, name=NAME_2,
                                         link=LINK_2)
            d3 = Document.objects.create(course=self, name=NAME_3,
                                         link=LINK_3)
            d4 = Document.objects.create(course=self, name=NAME_4,
                                         link=LINK_4)
            d5 = Document.objects.create(course=self, name=NAME_5,
                                         link=LINK_5)
            d6 = Document.objects.create(course=self, name=NAME_6,
                                         link=LINK_6)
            d7 = Document.objects.create(course=self, name=NAME_7,
                                         link=LINK_7)
            d8 = Document.objects.create(course=self, name=NAME_8,
                                         link=LINK_8)
            self.document_set.add(d1, d2, d3, d4, d5, d6, d7, d8)
            self.document_set.add(d1)
        super(Course, self).save(*args, **kwargs)

    def get_students(self):
        return self.userprofile_set.filter(profile_type='ST')

#     def get_students_without_team(self):
#         return self.userprofile_set.filter(profile_type='ST', in_team=False)

    def get_teams(self):
        return self.team_set.filter(course=self)

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


class Team(models.Model):
    '''
    Students log in as a team, teams hold progress.
    '''
    user = models.OneToOneField(User, related_name="team")
    course = models.ForeignKey(Course, null=True, default=None, blank=True)
    signed_contract = models.BooleanField(default=False)
    budget = models.PositiveIntegerField(default=65000)
    '''
    We need a plain text copy of the password to email the students
    '''
    team_passwd = models.CharField(max_length=255, default="", blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ["user"]

    def get_team_members(self):
        '''Should I explicitly set it to return
        only profiles of 'ST' type?'''
        return self.userprofile_set.all()


class UserProfile(models.Model):
    '''UserProfile adds extra information to a user,
    and associates the user with a course.'''
    user = models.OneToOneField(User, related_name="profile")
    profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)
    '''Leaving course null/blank because admins and
    teachers do not necessarily belong to a course.'''
    course = models.ForeignKey(Course, null=True, default=None, blank=True)
    team = models.ForeignKey(Team, null=True, default=None, blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ["user"]

    def display_name(self):
        return '%s - %s' % (self.user.first_name, self.user.last_name)

    def is_student(self):
        return self.profile_type == 'ST'

    def is_teacher(self):
        return self.profile_type == 'TE'

    def is_admin(self):
        return self.profile_type == 'AD'

    def role(self):
        if self.is_student():
            return "student"
        elif self.is_teacher():
            return "faculty"
        elif self.is_admin():
            return "administrator"


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

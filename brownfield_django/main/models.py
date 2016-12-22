from django.db import models
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
        super(Course, self).save(*args, **kwargs)
        if self.document_set.count() == 0:
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
            '''This is completely redundant but flake8 is going to
            whine about it...'''
            self.document_set.add(d1, d2, d3, d4, d5, d6, d7, d8)

    def get_students(self):
        return self.userprofile_set.filter(profile_type='ST')

    def get_student_users(self):
        profile_set = self.get_students()
        user_set = User.objects.filter(profile__in=profile_set)
        return user_set

    def get_teams(self):
        return self.team_set.filter(course=self)

    def get_documents(self):
        documents = Document.objects.filter(course=self)
        return documents


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
    user = models.OneToOneField(User, null=True, default=None,
                                blank=True, related_name="team")
    course = models.ForeignKey(Course, null=True, default=None, blank=True)
    signed_contract = models.BooleanField(default=False)
    budget = models.PositiveIntegerField(default=65000)
    '''
    We need a plain text copy of the password to email the students
    '''
    team_passwd = models.CharField(max_length=255, default="", blank=True)

    def __unicode__(self):
        name = ""
        try:
            name = self.user.username
        except:
            name = "TeamUser"
        return name

    class Meta:
        ordering = ["user"]

    def get_team_members(self):
        '''Should I explicitly set it to return
        only profiles of 'ST' type?'''
        return self.userprofile_set.all()

    def get_team_history(self):
        history = History.objects.filter(team=self)
        return history


class UserProfile(models.Model):
    '''UserProfile adds extra information to a user,
    and associates the user with a course.'''
    user = models.OneToOneField(User, related_name="profile")
    profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)
    '''Leaving course null/blank because admins and
    teachers do not necessarily belong to a course.'''
    archive = models.BooleanField(default=False)
    course = models.ForeignKey(Course, null=True, default=None, blank=True)
    team = models.ForeignKey(Team, null=True, default=None, blank=True)
    tmp_passwd = models.CharField(max_length=255, default="", blank=True)

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
        if self.is_admin():
            return "administrator"
        elif self.is_teacher():
            return "faculty"
        else:
            return "student"

    def get_absolute_url(self):
        if self.is_teacher():
            return '/ccnmtl/home/%s/' % (self.id)
        if self.is_admin():
            return '/ccnmtl/home/%s/' % (self.id)
        return '/'


class History(models.Model):
    team = models.ForeignKey(Team)
    date = models.CharField(max_length=16)
    # date = models.DateTimeField(default=datetime.now())
    description = models.CharField(max_length=255)
    cost = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s - %s' % (self.description, self.team)

    def get_tests_performed(self):
        performed_tests = PerformedTest.objects.filter(history=self)
        return performed_tests

    def get_information(self):
        information = Information.objects.filter(history=self)
        return information


class PerformedTest(models.Model):
    history = models.ForeignKey(History, null=True, default=None, blank=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    testDetails = models.CharField(default="", max_length=255)
    testNumber = models.IntegerField(default=0)
    paramString = models.CharField(default="", max_length=255)

    def __unicode__(self):
        return '%s - %s' % (self.testDetails, self.paramString)


class Information(models.Model):
    """
    Comment from Old Code:
        Documents and News Items made available to or found by the Team
    """
    history = models.ForeignKey(History, null=True, default=None, blank=True)
    infoType = models.CharField(default="", max_length=255, blank=True)
    internalName = models.CharField(default="", max_length=255, blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.infoType, self.internalName)

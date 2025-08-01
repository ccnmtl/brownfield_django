from django.contrib.auth.models import User
from django.db import models

from brownfield_django.main.document_links import all_documents


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
    created_at = models.DateTimeField(auto_now_add=True)
    professor = models.ForeignKey(User, related_name="taught_by", null=True,
                                  default=None, blank=True,
                                  on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Course, self).save(*args, **kwargs)
        if self.document_set.count() == 0:
            for doc in all_documents:
                d = Document.objects.create(
                    course=self, name=doc['name'], link=doc['link'])
                self.document_set.add(d)

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
                               default=None, blank=True,
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    link = models.CharField(max_length=255, default='')
    visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']


class Team(models.Model):
    '''
    Students log in as a team, teams hold progress.
    '''
    user = models.OneToOneField(User, null=True, default=None,
                                blank=True, related_name="team",
                                on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, default=None, blank=True,
                               on_delete=models.CASCADE)
    signed_contract = models.BooleanField(default=False)
    budget = models.PositiveIntegerField(default=65000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    '''
    We need a plain text copy of the password to email the students
    '''
    team_passwd = models.CharField(max_length=255, default="", blank=True)

    def __str__(self):
        name = ""
        try:
            name = self.user.username
        except AttributeError:
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
    user = models.OneToOneField(User, related_name="profile",
                                on_delete=models.CASCADE)
    profile_type = models.CharField(max_length=2, choices=PROFILE_CHOICES)
    '''Leaving course null/blank because admins and
    teachers do not necessarily belong to a course.'''
    archive = models.BooleanField(default=False)
    course = models.ForeignKey(Course, null=True, default=None, blank=True,
                               on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, default=None, blank=True,
                             on_delete=models.CASCADE)
    tmp_passwd = models.CharField(max_length=255, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
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
        # Note that a url of '/' can trigger a redirect loop in HomeView.
        url = '/'

        if self.is_teacher() or self.is_admin():
            url = '/ccnmtl/home/%s/' % (self.id)
        else:
            team = Team.objects.get(user=self.user.pk)
            url = '/team/home/%s/' % (team.pk)

        return url


class History(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date = models.CharField(max_length=16)
    description = models.TextField()
    cost = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.description, self.team)

    def get_tests_performed(self):
        performed_tests = PerformedTest.objects.filter(history=self)
        return performed_tests

    def get_information(self):
        information = Information.objects.filter(history=self)
        return information


class PerformedTest(models.Model):
    history = models.ForeignKey(History, null=True, default=None, blank=True,
                                on_delete=models.CASCADE)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    testDetails = models.CharField(default="", max_length=255)
    testNumber = models.IntegerField(default=0)
    paramString = models.CharField(default="", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.testDetails, self.paramString)


class Information(models.Model):
    """
    Comment from Old Code:
        Documents and News Items made available to or found by the Team
    """
    history = models.ForeignKey(History, null=True, default=None, blank=True,
                                on_delete=models.CASCADE)
    infoType = models.CharField(default="", max_length=255, blank=True)
    internalName = models.CharField(default="", max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.infoType, self.internalName)

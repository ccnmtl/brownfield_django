import factory
from datetime import datetime
from django.contrib.auth.models import User
from brownfield_django.main.models import Document, Course, \
    UserProfile, History, PerformedTest


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: "user%d" % n)
    password = factory.PostGenerationMethodCall('set_password', 'test')


class CourseFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Course
    name = "Test Course"
    password = "12345"
    startingBudget = 65000
    enableNarrative = True
    message = "Hello you non existant students."
    active = True
    professor = factory.SubFactory(UserFactory)


class DocumentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Document
    name = "Test Document for Course"
    course = factory.SubFactory(CourseFactory)
    link = "<a href='/path/to/the/course/document/here'></a>"
    visible = False


class UserProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory(UserFactory)
    profile_type = 'TM'
    course = factory.SubFactory(CourseFactory)


class TeamProfileFactory(UserProfileFactory):
    profile_type = 'TM'


class TeacherProfileFactory(UserProfileFactory):
    user = factory.SubFactory(UserFactory)
    profile_type = 'TE'


class AdminProfileFactory(UserProfileFactory):
    user = factory.SubFactory(UserFactory)
    profile_type = 'AD'


class CourseOneFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Course
    name = "Test Course One"
    password = "12345"
    startingBudget = 65000
    enableNarrative = True
    message = "Hello you non existant students."
    active = True
    professor = factory.SubFactory(UserFactory)


class CourseTwoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Course
    name = "Test Course Two"
    password = "12345"
    startingBudget = 65000
    enableNarrative = True
    message = "Hello you non existant students."
    active = True
    professor = factory.SubFactory(UserFactory)


class HistoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = History
    team = factory.SubFactory(TeamProfileFactory)
    date = datetime.now()
    description = "History Record"
    cost = 100


class PerformedTestFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PerformedTest
    X = 10
    y = 30
    z = 60
    testNumber = 1
    paramString = '''Still need to find format for these...'''

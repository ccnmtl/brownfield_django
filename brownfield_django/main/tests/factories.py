import factory
from django.contrib.auth.models import User
from brownfield_django.main.models import Document, Course, \
    UserProfile, History, PerformedTest, Team, Information


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: "user%d" % n)
    password = factory.PostGenerationMethodCall('set_password', 'test')


class CourseFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Course
    name = "Test Course"
    startingBudget = 65000
    enableNarrative = True
    message = "Hello you non existent students."
    active = True


class TeamFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Team
    team_passwd = "test"


class DocumentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Document
    name = "Test Document for Course"
    link = "<a href='/path/to/the/course/document/here'></a>"
    visible = False


class UserProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory(UserFactory)
    profile_type = 'ST'


class HistoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = History
    team = factory.SubFactory(TeamFactory)
    date = '2014/10/23 13:14'
    description = "History Record"
    cost = 100


class PerformedTestFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PerformedTest
    history = factory.SubFactory(HistoryFactory)
    x = 10
    y = 30
    z = 60
    testNumber = 1
    paramString = '''Still need to find format for these...'''
    testDetails = "Test Details Here..."


class InformationTestFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Information
    history = factory.SubFactory(HistoryFactory)
    infoType = "recon"
    internalName = "recon"

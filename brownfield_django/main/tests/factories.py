import factory
from datetime import datetime
from django.contrib.auth.models import User
from brownfield_django.main.models import Document, Course, Team, UserProfile, \
    History, PerformedTest


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
    creator = factory.SubFactory(UserFactory)


class UserProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory(UserFactory)
    profile_type = 'ST'
    # defaulting to student well get
    #more specific in following facorties
    course = factory.SubFactory(CourseFactory)


class StudentProfileFactory(UserProfileFactory):
    profile_type = 'ST'


class TeacherProfileFactory(UserProfileFactory):
    profile_type = 'TE'

'''Not entirely sure I even need a userprofile team
team model may be more appropriate'''
# class TeamFactory(factory.DjangoModelFactory):
#     FACTORY_FOR = School
#     country = factory.SubFactory(CountryFactory)
#     name = factory.Sequence(lambda n: "school %d" % n)


class TeamFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Team
    name = "Team One"
    course = factory.SubFactory(CourseFactory)
    team_entity = factory.SubFactory(UserFactory)
    signed_contract = False
    budget = "65000"


class HistoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = History
    team = factory.SubFactory(TeamFactory)
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
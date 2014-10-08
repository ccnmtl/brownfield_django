# from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User

from factories import UserFactory, UserProfileFactory, TeacherProfileFactory, \
    TeamProfileFactory, CourseFactory, HistoryFactory, \
    PerformedTestFactory, DocumentFactory, AdminProfileFactory, \
    StudentProfileFactoryOne, StudentProfileFactoryTwo

from brownfield_django.main.models import CourseForm


class TestUserFactory(TestCase):

    def test_unicode(self):
        user = UserFactory()
        self.assertEqual(str(user), user.username)


class TestCourseFactory(TestCase):

    def test_unicode(self):
        course = CourseFactory()
        self.assertEqual(str(course), course.name)


class TestHistoryFactory(TestCase):

    def test_unicode(self):
        his = HistoryFactory()
        self.assertEqual(str(his), '%s - %s' % (his.description, his.team))


class TestPerformedTestFactory(TestCase):

    def test_unicode(self):
        pt = PerformedTestFactory()
        self.assertEqual(str(pt), pt.paramString)


class TestUserProfileFactory(TestCase):

    def test_unicode(self):
        up = UserProfileFactory()
        self.assertEqual(str(up), up.user.username)


class TestAdminProfileFactory(TestCase):

    def test_unicode(self):
        admin = AdminProfileFactory()
        self.assertEqual(str(admin), admin.user.username)
        self.assertEqual(admin.role(), "administrator")
        self.assertEqual(admin.is_admin(), True)
        self.assertEqual(admin.is_team(), False)


class TestTeacherProfileFactory(TestCase):

    def test_unicode(self):
        teach = TeacherProfileFactory()
        self.assertEqual(str(teach), teach.user.username)
        self.assertEqual(teach.role(), "faculty")
        self.assertEqual(teach.is_teacher(), True)
        self.assertEqual(teach.is_team(), False)


class TestTeamProfileFactory(TestCase):
    def test_unicode(self):
        team = TeamProfileFactory()
        self.assertEqual(str(team), team.user.username)
        self.assertEqual(team.role(), "team")
        self.assertEqual(team.is_team(), True)
        self.assertEqual(team.is_teacher(), False)


class TestCourseMethods(TestCase):
    '''
    Course model has several helper methods to assist
    in retrieving data for the dashboard.
    '''

    def test_course_get_students(self):
        '''
        Create some students, add to course. Make sure
        students are returned when get_students
        is called on course.
        '''
        student_one = StudentProfileFactoryOne()
        student_two = StudentProfileFactoryTwo()
        course = CourseFactory()
        course.userprofile_set.add(student_one, student_two)
        self.assertTrue(student_one in course.get_students())
        self.assertTrue(student_two in course.get_students())

    def test_course_get_teams(self):
        '''Create team and add to course, make sure
        get teams returns the team from the course.'''
        team = TeamProfileFactory()
        course = CourseFactory()
        course.userprofile_set.add(team)
        self.assertTrue(team in course.get_teams())

    def test_course_get_documents(self):
        '''Right now the documents are added in the view,
        so we must add them here manually.'''
        document1 = DocumentFactory()
        document2 = DocumentFactory()
        document3 = DocumentFactory()
        course = CourseFactory()
        course.document_set.add(document1)
        course.document_set.add(document2)
        course.document_set.add(document3)
        self.assertTrue(document1 in course.get_documents())
        self.assertTrue(document2 in course.get_documents())
        self.assertTrue(document3 in course.get_documents())

    def test_course_get_form(self):
        '''Make sure get_form returns a course form.'''
        course = CourseFactory()
        form = course.get_course_form()
        course_form = CourseForm()
        self.assertEqual(type(course_form), type(course.get_course_form()))

#  def get_students_without_team(self):
#         return self.userprofile_set.filter(profile_type='ST', in_team=False)
#     
#     def get_teams(self):
#         return self.userprofile_set.filter(profile_type='TM')
#     
#     def get_team_members(self, name):
#         return self.userprofile_set.filter(profile_type='ST', team_name=name)
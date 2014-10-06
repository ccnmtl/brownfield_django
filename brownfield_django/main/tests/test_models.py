# from datetime import date

from django.test import TestCase
# from django.contrib.auth.models import User

from factories import UserFactory, UserProfileFactory, TeacherProfileFactory, \
    TeamProfileFactory, CourseFactory, HistoryFactory, \
    PerformedTestFactory


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


class TestTeacherProfileFactory(TestCase):
    def test_unicode(self):
        teach = TeacherProfileFactory()
        self.assertEqual(str(teach), teach.user.username)


class TestTeamProfileFactory(TestCase):
    def test_unicode(self):
        team = TeamProfileFactory()
        self.assertEqual(str(team), team.user.username)


class TestCourseMethods(TestCase):

    def test_course_get_teams(self):
        team = TeamProfileFactory()
        course = CourseFactory()
        course.userprofile_set.add(team)
        self.assertTrue(team in course.get_teams())

    def test_course_get_documents(self):
        team = TeamProfileFactory()
        course = CourseFactory()
        course.userprofile_set.add(team)
        self.assertTrue(team in course.get_teams())
        documents = Document.objects.filter(course=self)
        return documents

    def test_course_get_form(self):
        team = TeamProfileFactory()
        course = CourseFactory()
        course.userprofile_set.add(team)
        self.assertTrue(team in course.get_teams())
        form = CourseForm()
        return form



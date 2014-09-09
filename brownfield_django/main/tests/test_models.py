from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User

from factories import UserFactory, UserProfileFactory, TeacherProfileFactory, \
    StudentProfileFactory, CourseFactory, TeamFactory


class TestCourseFactory(TestCase):
    def test_unicode(self):
        course = CourseFactory()
        self.assertEqual(str(course), course.name)


class TestTeamFactory(TestCase):
    def test_unicode(self):
        team = TeamFactory()
        self.assertEqual(str(team), team.name)

# 
# class TestUserProfileFactory(TestCase):
#     def test_unicode(self):
#         up = UserProfileFactory()
#         self.assertEqual(str(up), up.user.username)


# class TestTeacherProfileFactory(TestCase):
#     def test_unicode(self):
#         teach = TeacherProfileFactory()
#         self.assertEqual(str(teach), teach.user.username)
# 
# 
# class TestStudentProfileFactory(TestCase):
#     def test_unicode(self):
#         student = StudentProfileFactory()
#         self.assertEqual(str(student), student.user.username)











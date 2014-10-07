# import json
# from datetime import datetime

from django.test import TestCase, RequestFactory
from django.test.client import Client
# from django.contrib.auth.models import User

# from pagetree.helpers import get_hierarchy

#from factories import TeacherProfileFactory, \
#    CourseOneFactory, CourseTwoFactory
# , \ UserFactory, UserProfileFactory,
#    StudentProfileFactory, CourseFactory, TeamFactory


#class TestInstructorLogin(TestCase):

#    def setUp(self):
#        self.client = Client()
#        self.factory = RequestFactory()
#        self.teacher = TeacherProfileFactory().user
#        self.course_one = CourseOneFactory()
#         self.course_two = CourseTwoFactory()
#         self.client.login(username=self.teacher.username, password="test")

#    def test_home(self):
#        pass
#         response = self.client.get("/", follow=True)
#         self.assertEquals(
#             response.redirect_chain[0],
#             ('http://testserver/teacher/' +
#              str(self.teacher.profile.pk) + '/',
#              302))
#         self.assertTemplateUsed(response,
#                                 'main/instructor/instructor_home.html')

#    def test_post_course(self):
#        '''
#        Calling post with desired name of the new course
#        should result in a new course with that name being created
#        and the course info (key) being returned to the browser to update
#        the course list.
#        '''
#        pass

#    def test_get_course(self):
#        '''
#        Calling get for a course should redirect the instructor to a
#        course detail page where they can create teams, add students,
#        and put students in teams.
#        '''
#        pass

#    def test_update_course(self):
#        '''
#        Calling get for a course should redirect the instructor to a
#        course detail page where they can create teams, add students,
#        and put students in teams.
#        '''
#        pass

#    def test_remove_course(self):
#        '''
#        Calling get for a course should redirect the instructor to a
#        course detail page where they can create teams, add students,
#        and put students in teams.
#        '''
#        pass

#    '''Test document related urls'''

#    def test_post_document(self):
#        '''
#        Calling post with desired name of the new course
#        should result in a new course with that name being created
#        and the course info (key) being returned to the browser to update
#        the course list.
#        '''
#        pass

#    def test_get_document(self):
#        '''
#        Calling get for a course should redirect the instructor to a
#        course detail page where they can create teams, add students,
#        and put students in teams.
#        '''
#        pass

#    '''Test team related urls'''
#
#    def test_post_team(self):
#        '''
#        Calling post with desired name of the new course
#        should result in a new course with that name being created
#        and the course info (key) being returned to the browser to update
#        the course list.
#        '''
#        pass

#    def test_get_team(self):
#        '''
#        Calling get for a course should redirect the instructor to a
#        course detail page where they can create teams, add students,
#        and put students in teams.
#        '''
#        pass

#    def test_update_team(self):
#        '''
#        Calling get for a course should redirect the instructor to a
#        course detail page where they can create teams, add students,
#        and put students in teams.
#        '''
#        pass

#    def teamtest_remove_course(self):
#        '''
#        Calling get for a course should redirect the instructor to a
#        course detail page where they can create teams, add students,
#        and put students in teams.
#        '''
#        pass

#    '''Test student related urls'''

#    def test_post_student(self):
#        '''
#        Calling post with desired name of the new course
#        should result in a new course with that name being created
#        and the course info (key) being returned to the browser to update
#        the course list.
#        '''
#        pass

#    def test_get_student(self):
#        '''
#        Calling get for a course should redirect the instructor to a
#        course detail page where they can create teams, add students,
#        and put students in teams.
#        '''
#        pass

#    def test_update_student(self):
#        '''
#        Calling get for a course should redirect the instructor to a
#        course detail page where they can create teams, add students,
#        and put students in teams.
#        '''
#        pass

#    def test_remove_student(self):
#        '''
#        Calling get for a course should redirect the instructor to a
#        course detail page where they can create teams, add students,
#        and put students in teams.
#        '''
#        pass

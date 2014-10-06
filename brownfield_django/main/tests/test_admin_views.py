# import json
# from datetime import datetime

from django.test import TestCase, RequestFactory
from django.test.client import Client
# from django.contrib.auth.models import User

from factories import AdminProfileFactory  # , \
#    CourseOneFactory, CourseTwoFactory
# , \ UserFactory, UserProfileFactory,
#    StudentProfileFactory, CourseFactory, TeamFactory


class TestAdminLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.admin = AdminProfileFactory().user
        self.client.login(username=self.admin.username, password="test")

    def test_home_redirect(self):
        '''Keep getting random bootstrap can't be compressed errors.'''
        request = self.client.get("/", follow=True)
        self.assertEquals(
            response.redirect_chain[0],
            ('http://testserver/ccnmtl/' +
             str(self.admin.profile.pk) + '/',
             302))
        self.assertTemplateUsed(response,
                                'main/ccnmtl/ccnmtl_home.html')

    def test_home(self):
        '''
        See what happens if I request appropriate home directly
        instead of following redirect.
        '''
        request = self.client.get("/ccnmtl/" +
                                  str(self.admin.profile.pk) + '/')
        self.assertTemplateUsed(request,
                                'main/ccnmtl/ccnmtl_home.html')

    def test_add_course_by_name(self):
        '''
        Calling post with desired name of the new course
        should result in a new course with that name being created
        and the course info (key) being returned to the browser to update
        the course list.
        '''
        request = self.client.post("/course/")
        # self.assertTemplateUsed(request,
        #                        'main/ccnmtl/ccnmtl_home.html')

    def test_get_courses(self):
        '''
        Return list of courses - those the admin user
        created and all others.
        '''
        pass

    def test_get_course_details(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        request = self.client.get("/ccnmtl/" +
                                  str(self.admin.profile.pk) + '/')
        self.assertTemplateUsed(request,
                                'main/ccnmtl/ccnmtl_home.html')

    def test_update_course(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

    def test_remove_course(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

    '''Test document related urls'''

    def test_post_document(self):
        '''
        Calling post with desired name of the new course
        should result in a new course with that name being created
        and the course info (key) being returned to the browser to update
        the course list.
        '''
        pass

    def test_get_document(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

    '''Test team related urls'''

    def test_post_team(self):
        '''
        Calling post with desired name of the new course
        should result in a new course with that name being created
        and the course info (key) being returned to the browser to update
        the course list.
        '''
        pass

    def test_get_team(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

    def test_update_team(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

    def teamtest_remove_course(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

    '''Test student related urls'''

    def test_post_student(self):
        '''
        Calling post with desired name of the new course
        should result in a new course with that name being created
        and the course info (key) being returned to the browser to update
        the course list.
        '''
        pass

    def test_get_student(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

    def test_update_student(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

    def test_remove_student(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

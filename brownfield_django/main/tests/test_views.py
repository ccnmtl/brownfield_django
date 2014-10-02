# import json
# from datetime import datetime

from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.contrib.auth.models import User

from pagetree.helpers import get_hierarchy

from factories import TeacherProfileFactory, \
    CourseOneFactory, CourseTwoFactory
# , \ UserFactory, UserProfileFactory,
#    StudentProfileFactory, CourseFactory, TeamFactory

'''
Need to test:
    HomeView
    RegistrationView
    StudentHomeView
    TeamHomeView
    TeacherHomeView
    TeacherAddStudent
    TeacherCreateCourse
    TeacherDeleteCourse
    TeacherAddStudent
    TeacherReleaseDocument
    TeacherRevokeDocument
    TeamPreformTest
    OnLoad
    OnSave
'''


class BasicTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 302)
        # we want it to redirect to login,
        # that is current behavior of site

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)
        assert "PASS" in response.content


class PagetreeViewTestsLoggedOut(TestCase):
    def setUp(self):
        self.c = Client()
        self.h = get_hierarchy("main", "/pages/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })

    def test_page(self):
        r = self.c.get("/pages/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_edit_page(self):
        r = self.c.get("/pages/edit/section-1/")
        self.assertEqual(r.status_code, 302)

    def test_instructor_page(self):
        r = self.c.get("/pages/instructor/section-1/")
        self.assertEqual(r.status_code, 302)


class PagetreeViewTestsLoggedIn(TestCase):
    def setUp(self):
        self.c = Client()
        self.h = get_hierarchy("main", "/pages/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")

    def test_page(self):
        r = self.c.get("/pages/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_edit_page(self):
        r = self.c.get("/pages/edit/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_instructor_page(self):
        r = self.c.get("/pages/instructor/section-1/")
        self.assertEqual(r.status_code, 200)


class TestAnnonymousUserLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_home(self):
        response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.redirect_chain[0],
                          ('http://testserver/accounts/login/?next=/', 302))


class TestStudentUserLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()



class TestInstructorLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.teacher = TeacherProfileFactory().user
        self.course_one = CourseOneFactory()
        self.course_two = CourseTwoFactory()
        self.client.login(username=self.teacher.username, password="test")

    def test_home(self):
        response = self.client.get("/", follow=True)
        self.assertEquals(
            response.redirect_chain[0],
            ('http://testserver/teacher/' +
             str(self.teacher.profile.pk) + '/',
             302))
        self.assertTemplateUsed(response,
                                'main/instructor/instructor_home.html')

    def test_post_course(self):
        '''
        Calling post with desired name of the new course
        should result in a new course with that name being created
        and the course info (key) being returned to the browser to update
        the course list.
        '''
        pass

    def test_get_course(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

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

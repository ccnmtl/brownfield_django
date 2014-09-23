import json
from datetime import datetime

from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.contrib.auth.models import User

from pagetree.helpers import get_hierarchy

from factories import UserFactory, UserProfileFactory, TeacherProfileFactory, \
    StudentProfileFactory, CourseFactory, TeamFactory

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
        self.student = StudentProfileFactory().user
        self.client.login(username=self.student.username, password="test")

#     def test_home(self):
#         response = self.client.get("/", follow=True)
        #self.assertEquals(response.redirect_chain[0],[
        #                  ('http://testserver/student/'+str(self.student.pk), 302)])
        #self.assertTemplateUsed(response, 'main/student/student_home.html')
        

#     def test_home_noprofile(self):
#         user = UserFactory()
#         self.client.login(username=user.username, password="test")
# 
#         response = self.client.get("/", follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertEquals(response.redirect_chain[0],
#                           ('http://testserver/register/', 302))
# 
#     def test_dashboard(self):
#         response = self.client.get('/dashboard/')
#         self.assertEquals(response.status_code, 200)
# 
#     def test_dashboard_context(self):
#         request = RequestFactory().get('/dashboard/')
#         request.user = self.student
# 
#         view = UserProfileView()
#         view.request = request
# 
#         self.assertEquals(view.get_object(), request.user.profile)
# 
#         view.object = request.user.profile
#         ctx = view.get_context_data()
# 
#         self.assertEquals(ctx['optionb'], self.hierarchy)
#         self.assertIsNotNone(ctx['profile_form'])
#         self.assertEquals(ctx['countries'], COUNTRY_CHOICES)
#         self.assertEquals(ctx['joined_groups'].count(), 0)
#         self.assertTrue('managed_groups' not in ctx)
#         self.assertTrue('pending_teachers' not in ctx)
# 
# 
# 
# # 
# # 
# class TestTeacherUserLogin(TestCase):
#  
#     def setUp(self):
#         self.client = Client()
#         self.factory = RequestFactory()
#         self.student = TeacherProfileFactory().user
#         self.client.login(username=self.student.username, password="test")
#  
#     def test_home(self):
#         response = self.client.get("/", follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertEquals(response.redirect_chain[0],
#                           ('http://testserver/accounts/login/?next=/', 302))
#  
#  
#  
# 
# class TestStudentUserLogin(TestCase):
# 
#     def setUp(self):
#         self.client = Client()
#         self.factory = RequestFactory()
# 
# 
#     def test_home(self):
#         response = self.client.get("/", follow=True)
#         self.assertEquals(response.redirect_chain[0],[
#                           ('http://testserver/student/'+str(self.student.pk), 302)])
#         self.assertTemplateUsed(response, 'main/student/student_home.html')












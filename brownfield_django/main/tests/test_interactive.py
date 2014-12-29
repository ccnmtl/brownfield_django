from django.test import TestCase
from django.test.client import Client
from factories import UserFactory, UserProfileFactory
from brownfield_django.main.xml_strings import INITIAL_XML
 
 
class TestAdminInfoInteractiveViews(TestCase):
 
    def setUp(self):
        self.client = Client()
        self.admin = UserProfileFactory(user=UserFactory(username='admin'),
                                        profile_type='AD')
        self.client.login(username=self.admin.user.username, password="test")
 
    def test_admin_info_get_interaction(self):
        response = self.client.get("/demo/info/")
        self.assertEqual(response.content,
                         "<data><response>OK</response></data>")
 
    def test_admin_info_post_interaction(self):
        response = self.client.post("/demo/info/")
        self.assertEqual(response.content,
                         "<data><response>OK</response></data>")
 
 
# class TestInstructorInfoInteractiveViews(TestCase):
# 
#     def setUp(self):
#         self.client = Client()
#         self.factory = RequestFactory()
#         self.inst = ViewsTeacherProfileFactory().user
#         self.client.login(username=self.inst.username, password="Teacher")
# 
#     def test_instructor_info_get_interaction(self):
#         response = self.client.get("/demo/info/")
#         self.assertEqual(response.content, INITIAL_XML)
# 
#     def test_instructor_info_post_interaction(self):
#         response = self.client.post("/demo/info/")
#         self.assertEqual(response.content,
#                          "<data><response>OK</response></data>")
# 
# 
# class TestAdminHistoryInteractiveViews(TestCase):
# 
#     def setUp(self):
#         self.client = Client()
#         self.factory = RequestFactory()
#         self.admin = ViewsAdminProfileFactory().user
#         self.client.login(username=self.admin.username, password="Admin")
# 
#     def test_admin_history_get_interaction(self):
#         response = self.client.get("/demo/history/")
#         self.assertEqual(response.content, INITIAL_XML)
# 
#     def test_admin_history_post_interaction(self):
#         response = self.client.post("/demo/history/")
#         self.assertEqual(response.content, INITIAL_XML)
# 
# 
# class TestInstructorHistoryInteractiveViews(TestCase):
# 
#     def setUp(self):
#         self.client = Client()
#         self.factory = RequestFactory()
#         self.inst = ViewsTeacherProfileFactory().user
#         self.client.login(username=self.inst.username, password="Teacher")
# 
#     def test_instructor_history_get_interaction(self):
#         response = self.client.get("/demo/history/")
#         self.assertEqual(response.content, INITIAL_XML)
# 
#     def test_instructor_history_post_interaction(self):
#         response = self.client.post("/demo/history/")
#         self.assertEqual(response.content, INITIAL_XML)
# 
# 
# class TestAdminTestInteractiveViews(TestCase):
# 
#     def setUp(self):
#         self.client = Client()
#         self.factory = RequestFactory()
#         self.admin = ViewsAdminProfileFactory().user
#         self.client.login(username=self.admin.username, password="Admin")
# 
#     def test_admin_test_get_interaction(self):
#         response = self.client.get("/demo/test/")
#         self.assertEqual(response.content, INITIAL_XML)
# 
#     def test_admin_test_post_interaction(self):
#         response = self.client.post("/demo/test/")
#         self.assertEqual(response.content, INITIAL_XML)
# 
# 
# class TestInstructorTestInteractiveViews(TestCase):
# 
#     def setUp(self):
#         self.client = Client()
#         self.factory = RequestFactory()
#         self.inst = ViewsTeacherProfileFactory().user
#         self.client.login(username=self.inst.username, password="Teacher")
# 
#     def test_test_history_get_interaction(self):
#         response = self.client.get("/demo/test/")
#         self.assertEqual(response.content, INITIAL_XML)
# 
#     def test_test_history_post_interaction(self):
#         response = self.client.post("/demo/test/")
#         self.assertEqual(response.content, INITIAL_XML)

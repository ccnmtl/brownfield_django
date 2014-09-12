import json

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, RequestFactory
from django.test.client import Client
'''
Starting with tests from old app
'''

class TestInstructorViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_create_course(self):
        response = self.client.post('/create_course/',
                                    {"startingBudget": 60000,
                                     "enableNarrative": True})
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed('flatpages/about.html')


    def test_create_team(self):
        response = self.client.post('/create_team/1/team/',
                                    {"name": "Alpha"})
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed('flatpages/about.html')
        
        
        
        
class TestTeamViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_create_min_test_record(self):
        '''======Send a test with the minimum fields======'''
        response = self.client.post('/course/1/team/1/test',
                                    {"cachebuster": "0.594946100376546",#0%2E594946100376546,
                                     "description": "put description here",
                                     "date": "put description here",
                                     "cost": "1500",
                                     "y": "1350",
                                     "x": "720",
                                     "testNumber": "8",
                                     "authkey": "enbwzfeqrsxtphevnnjnduqbyjxouh",
                                     })
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed('flatpages/about.html')

    def test_create_max_test_record(self):
        '''======Send a test with all the fields possible======'''
        response = self.client.post('/course/1/team/1/test',
                                    {"cachebuster": "0.594946100376546",#0%2E594946100376546,
                                     "description": "Excavation at 720 1350",
                                     "date": "2007/1/26 16:12",
                                     "cost": "1500",
                                     "y": "1350",
                                     "x": "720",
                                     "z": "120",
                                     "testNumber": "8",
                                     "paramString": "blahblah",
                                     "authkey": "enbwzfeqrsxtphevnnjnduqbyjxouh",
                                     })
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed('flatpages/about.html')

    def test_create_test_record(self):
        '''======Send a test with all the fields possible======'''
        response = self.client.post('/course/1/team/1/test',
                                    {"cachebuster": "0.594946100376546",#0%2E594946100376546,
                                     "description": "Excavation at 720 1350",
                                     "date": "2007/1/26 16:12",
                                     "cost": "1500",
                                     "y": "1350",
                                     "x": "720",
                                     "z": "120",
                                     "testNumber": "8",
                                     "paramString": "blahblah",
                                     "authkey": "enbwzfeqrsxtphevnnjnduqbyjxouh",
                                     })
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed('flatpages/about.html')

# &=blahblah\

# " $ROOT_URL/course/1/team/1/test
# 
# echo
# echo ======Get the Flash Client data back the correct way======
# curl $ROOT_URL/course/1/team/1/history
# 
# echo
# echo ======Get the Flash Client data the deprecated way======
# curl $ROOT_URL/course/1/team/1/history_old




# 
#         echo 
# curl -X "POST" --data "=\
# &=Excavation%20at%20720%2C%201350%2E\
# &=2007/1/26 16:12\


#     
#     def test_about(self):
#         response = self.client.get("/about/")
#         self.assertEquals(response.status_code, 200)
#         
# 
#     def test_help(self):
#         response = self.client.get("/help/")
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed('flatpages/help.html')
# 
#     def test_contact(self):
#         response = self.client.post('/contact/',
#                                     {"subject": "new_student",
#                                      "message": "new_student",
#                                      "sender": "new_student"})
#         self.assertEqual(response.status_code, 200)
# 
#     def test_contact_form_valid(self):
#         form = ContactForm()
#         form.cleaned_data = {
#             'first_name': 'Jane',
#             'last_name': 'Doe',
#             'sender': 'janedoe21@ccnmtl.columbia.edu',
#             'subject': 'Lorem Ipsum',
#             'message': 'Proin tristique volutpat purus sed accumsan.'
#         }
#         ContactView().form_valid(form)
#         self.assertEqual(len(mail.outbox), 1)
# 
#     def test_smoketest(self):
#         response = self.client.get("/smoketest/")
#         self.assertEquals(response.status_code, 200)
# 
# f = urllib.urlopen("http://localhost:8000/course/", params)
# print f.read()
# 
# 

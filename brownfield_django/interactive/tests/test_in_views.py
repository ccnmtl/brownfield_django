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
        data = {"cachebuster": "0.594946100376546",  # 0%2E594946100376546,
                "description": "put description here",
                "date": "put description here",
                "cost": "1500",
                "y": "1350",
                "x": "720",
                "testNumber": "8",
                "authkey": "enbwzfeqrsxtphevnnjnduqbyjxouh"}
        response = self.client.post('/course/1/team/1/test',
                                    data)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed('flatpages/about.html')

    def test_create_max_test_record(self):
        '''======Send a test with all the fields possible======'''
        data = {"cachebuster": "0.594946100376546",  # 0%2E594946100376546,
                "description": "Excavation at 720 1350",
                "date": "2007/1/26 16:12",
                "cost": "1500",
                "y": "1350",
                "x": "720",
                "z": "120",
                "testNumber": "8",
                "paramString": "blahblah",
                "authkey": "enbwzfeqrsxtphevnnjnduqbyjxouh"}
        response = self.client.post('/course/1/team/1/test',
                                    data)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed('flatpages/about.html')

    def test_create_test_record(self):
        data = {"cachebuster": "0.594946100376546",  # 0%2E594946100376546,
                "description": "Excavation at 720 1350",
                "date": "2007/1/26 16:12",
                "cost": "1500",
                "y": "1350",
                "x": "720",
                "z": "120",
                "testNumber": "8",
                "paramString": "blahblah",
                "authkey": "enbwzfeqrsxtphevnnjnduqbyjxouh"}
        response = self.client.post('/course/1/team/1/test', data)
        self.assertEqual(response.status_code, 200)

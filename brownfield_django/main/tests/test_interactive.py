from django.test import TestCase
from django.test.client import Client
from brownfield_django.main.xml_strings import INITIAL_XML


class TestDemoViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_info(self):
        response = self.client.get("/demo/info/")
        self.assertEqual(response.content, INITIAL_XML)

        response = self.client.post("/demo/info/")
        self.assertEqual(response.content,
                         "<data><response>OK</response></data>")

    def test_history(self):
        response = self.client.get("/demo/history/")
        self.assertEqual(response.content, INITIAL_XML)

        response = self.client.post("/demo/history/")
        self.assertEqual(response.content,
                         "<data><response>OK</response></data>")

    def test_test(self):
        response = self.client.get("/demo/test/")
        self.assertEqual(response.content, INITIAL_XML)

        response = self.client.post("/demo/test/")
        self.assertEqual(response.content,
                         "<data><response>OK</response></data>")

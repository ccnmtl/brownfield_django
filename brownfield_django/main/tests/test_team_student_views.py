from django.test import TestCase
from django.test.client import Client

from factories import UserProfileFactory, UserFactory, \
    CourseFactory, TeamFactory


class TestTeamViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.teacher = UserProfileFactory(user=UserFactory(username='teacher'),
                                          profile_type='TE')
        self.test_course = CourseFactory(professor=self.teacher.user,
                                         name='Test Course')
        self.team = TeamFactory(
            user=UserFactory(username='team', first_name='team'),
            course=self.test_course)
        self.client.login(username=self.team.user.username, password='test')

    def test_home(self):
        request = self.client.get("/team/home/" +
                                  str(self.team.pk) + '/')
        self.assertTemplateUsed(request,
                                'main/team/team_home.html')

    def test_initial_history(self):
        response = self.client.get("/team/" + str(self.team.user.pk) + "/play")
        self.assertTemplateUsed(response,
                                'main/team/history.txt')
        self.assertEqual(response.status_code, 200)

    def test_play_brownfield(self):
        '''Go through a series of requests to play the game as a team'''
        response = self.client.get("/team/" + str(self.team.user.pk) + "/play")
        self.assertTemplateUsed(response,
                                'main/team/history.txt')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            "/team/" + str(self.team.user.pk) + "/info/",
            {'infoType': 'recon', 'date': '2014/10/23 13:14',
             'description': 'performing reconnaissance', 'cost': '100',
             'internalName': 'recon internal info'})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            "/team/" + str(self.team.user.pk) + "/history/")
        self.assertTemplateUsed(response,
                                'main/team/bfaxml.txt')
        response = self.client.post(
            "/team/" + str(self.team.user.pk) + "/test/",
            {'x': '350', 'y': '450', 'testNumber': '2', 'z': '150',
             'date': '2014/10/23 13:14', 'testDetails': 'some_details_here',
             'paramString': 'some other values',
             'description': 'description goes here', 'cost': '200'})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            "/team/" + str(self.team.user.pk) + "/history/")
        self.assertTemplateUsed(response,
                                'main/team/bfaxml.txt')
        self.assertEqual(response.status_code, 200)

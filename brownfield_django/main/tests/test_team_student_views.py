from django.test import TestCase
from django.test.client import Client

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

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
            {'infoType': "recon", 'date': '2014/10/23 13:14',
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
        response = self.client.post(
            "/team/" + str(self.team.user.pk) + "/info/",
            {'infoType': "visit", 'date': '2014/10/23 13:14',
             'description': 'Visiting a site', 'cost': '25',
             'internalName': 'site visit'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            "/team/" + str(self.team.user.pk) + "/info/",
            {'infoType': "question", 'date': '2014/10/23 13:14',
             'description': 'Question person at site', 'cost': '1',
             'internalName': 'Question'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            "/team/" + str(self.team.user.pk) + "/info/",
            {'infoType': "doc", 'date': '2014/10/23 13:14',
             'description': 'Document description', 'cost': '2',
             'internalName': 'Document'})
        self.assertEqual(response.status_code, 200)


class TestStudentViews(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.teacher = UserProfileFactory(user=UserFactory(username='teacher'),
                                          profile_type='TE')
        self.test_course = CourseFactory(professor=self.teacher.user,
                                         name='Test Course')
        self.student = UserProfileFactory(user=UserFactory(username='student'),
                                          profile_type='ST',
                                          course=self.test_course)
        self.client.login(username=self.student.user.username, password='test')

    def test_no_courses(self):
        response = self.client.get("/api/course/")
        self.assertEqual(response.data, [])

    def test_no_documents(self):
        response = self.client.get("/api/document/")
        self.assertEqual(response.data, [])

    def test_user_is_self(self):
        '''Students can't actually log in, added checks to check each possible
        kind of profile to be thorough, so it is returning a team for the user
        url'''
        response = self.client.get("/api/user/")
        self.assertEqual(
            response.data,
            [{'url': 'http://testserver/api/eteam/' +
              str(self.student.pk) + '/',
              'username': self.student.user.username,
              'email': u''}])

    def test_no_students(self):
        response = self.client.get("/api/student/")
        self.assertEqual(response.data, [])

    def test_no_student_create(self):
        response = self.client.post("/api/student/")
        self.assertEqual(response.status_code, 403)

    def test_no_student_update(self):
        response = self.client.put("/api/student/" +
                                   str(self.student.user.pk) + "/")
        self.assertEqual(response.status_code, 403)

    def test_no_teams(self):
        response = self.client.get("/api/eteam/")
        self.assertEqual(response.data, [])

    def test_no_team_create(self):
        response = self.client.post("/api/eteam/")
        self.assertEqual(response.status_code, 403)

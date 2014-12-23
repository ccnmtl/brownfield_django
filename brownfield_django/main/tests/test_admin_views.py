from django.test import TestCase, RequestFactory
from django.test.client import Client

from factories import ViewsAdminProfileFactory, AdminUserCourseFactory, \
    StudentUserFactoryOne, StudentUserFactoryTwo, TeacherUserFactory

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient


class TestAdminViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.admin = ViewsAdminProfileFactory().user
        self.client.login(username=self.admin.username, password="Admin")

    def test_home(self):
        request = self.client.get("/ccnmtl/home/" +
                                  str(self.admin.profile.pk) + '/')
        self.assertTemplateUsed(request,
                                'main/ccnmtl/home_dash/ccnmtl_home.html')

    def test_get_course_details(self):
        '''
        Requesting the course details page should redirect
        the admin to a course dashboard where they can create
        teams and students, and put students in teams.
        '''
        self.admin_course = AdminUserCourseFactory()
        request = self.client.get("/course_details/" +
                                  str(self.admin_course.pk) + '/')
        self.assertTemplateUsed(request,
                                'main/ccnmtl/course_dash/course_home.html')


class TestCourseRestViews(APITestCase):
    '''Test course related urls'''

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.admin = ViewsAdminProfileFactory().user
        self.client.login(username=self.admin.username, password="Admin")

    def test_basic_get_courses(self):
        ''' Get all Course Documents. '''
        crs = AdminUserCourseFactory()
        response = self.client.get('/api/course/',
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         [{'id': 1,
                           'url': 'http://testserver/api/course/1/',
                           'name': u'Test Course',
                           'startingBudget': 65000,
                           'enableNarrative': True,
                           'message': u'Hello you non existent students.',
                           'active': True,
                           'archive': False,
                           'professor': 'http://testserver/api/instructor/1/'},
                          {'id': crs.id,
                           'url': 'http://testserver/api/course/2/',
                           'name': crs.name,
                           'startingBudget': crs.startingBudget,
                           'enableNarrative': True,
                           'message': u'Hello you non existent students.',
                           'active': True,
                           'archive': False,
                           'professor': 'http://testserver/api/instructor/3/'}
                          ])


class TestUserViewset(APITestCase):
    '''Test user viewset class'''

    def setUp(self):
        self.client = APIClient()
        self.admin = ViewsAdminProfileFactory().user
        self.client.login(username=self.admin.username, password="Admin")
        self.user_one = StudentUserFactoryOne()
        self.user_two = StudentUserFactoryTwo()
        self.user_three = TeacherUserFactory()

    def test_get_users_as_admin(self):
        ''' User is admin, should return list of all users '''
        response = self.client.get('/api/user/',
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [{'url': 'http://testserver/api/instructor/1/',
              # I can't figure out where this user is coming from???
              'username': u'user59', 'email': u''},
             {'url': 'http://testserver/api/instructor/2/',
              'username': self.admin.username, 'email': self.admin.email},
             {'url': 'http://testserver/api/instructor/3/',
              'username': self.user_one.username,
              'email': self.user_one.email},
             {'url': 'http://testserver/api/instructor/4/',
              'username': self.user_two.username,
              'email': self.user_two.email},
             {'url': 'http://testserver/api/instructor/5/',
              'username': self.user_three.username,
              'email': self.user_three.email}])


class TestDocumentRestViews(APITestCase):
    '''Test document related urls'''

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.admin = ViewsAdminProfileFactory().user
        self.client.login(username=self.admin.username, password="Admin")

    def test_get_documents(self):
        ''' Get all Course Documents. '''
        crs = AdminUserCourseFactory()
        response = self.client.get('/api/document/?course=' + str(crs.pk),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_release_revoke_document(self):
        ''' Release a document. '''
        crs = AdminUserCourseFactory()
        doc = crs.document_set.all()[0]
        response = self.client.put(
            '/api/document/' + str(doc.pk) + '/',
            {'id': doc.pk, 'name': u'Test Document for Admin',
             'link': u"<a href='/path/to/the/course/document/here'></a>",
             'visible': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, True)
        response = self.client.put(
            '/api/document/' + str(doc.pk) + '/', format='json')
        self.assertEqual(response.data, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestStudentRestViews(APITestCase):
    '''Test student related urls and methods, has GET, PUT/update,
    POST/create, DELETE/destroy'''

    def setUp(self):
        ''' Admin will log in, and navigate to a course page. '''
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.crs = AdminUserCourseFactory()
        self.admin = ViewsAdminProfileFactory().user
        self.client.login(username=self.admin.username, password="Admin")

    def test_get_students(self):
        ''' Any students in the course will be returned via GET '''
        response = self.client.get('/api/student/?course=' +
                                   str(self.crs.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''No students have been added so test
        response.data - should be empty'''
        self.assertEqual(response.data, [])

    def test_create_student(self):
        ''' Any students in the course will be returned via GET '''
        response = self.client.post('/api/student/?course=' + str(self.crs.pk),
                                    {'first_name': 'Student First Name',
                                     'last_name': 'Student Last Name',
                                     'email': 'studentemail@email.com'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        '''After student is created, it should return the student data
        in response.data'''
        # The student id should not be hard coded - manually look up?
        self.assertEqual(response.data, {'id': 4,
                                         'first_name': u'Student First Name',
                                         'last_name': u'Student Last Name',
                                         'email': u'studentemail@email.com'})

    def test_create_then_update_student(self):
        ''' Any students in the course will be returned via GET '''
        response = self.client.post('/api/student/?course=' + str(self.crs.pk),
                                    {'first_name': 'Student First Name',
                                     'last_name': 'Student Last Name',
                                     'email': 'studentemail@email.com'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        '''After student is created, it should return the student data
        in response.data'''
        self.assertEqual(response.data, {'id': 4,
                                         'first_name': u'Student First Name',
                                         'last_name': u'Student Last Name',
                                         'email': u'studentemail@email.com'})
        # need to update view possibly to return student data, although it
        # seems backbone doesn't need it, it is probably good for testing
        # and diagnostics, also change wrong status codes
        response = self.client.put('/api/student/4/',
                                   {'first_name': 'Edit First Name',
                                    'last_name': 'Edit Last Name',
                                    'email': 'editmail@email.com'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_update_delete_student(self):
        ''' Any students in the course will be returned via GET '''
        response = self.client.post('/api/student/?course=' + str(self.crs.pk),
                                    {'first_name': 'Student First Name',
                                     'last_name': 'Student Last Name',
                                     'email': 'studentemail@email.com'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        '''After student is created, it should return the student data
        in response.data'''
        self.assertEqual(response.data, {'id': 4,
                                         'first_name': u'Student First Name',
                                         'last_name': u'Student Last Name',
                                         'email': u'studentemail@email.com'})
        response = self.client.put('/api/student/4/',
                                   {'first_name': 'Edit First Name',
                                    'last_name': 'Edit Last Name',
                                    'email': 'editmail@email.com'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete('/api/student/4/', format='json')
        # is there as success code for delete?
        # should I test the models to see if they were deleted as well?
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTeamRestViews(APITestCase):
    '''Test team related urls and methods, has GET, PUT/update,
    POST/create, DELETE/destroy'''

    def setUp(self):
        ''' Admin will log in, and navigate to a course page. '''
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.crs = AdminUserCourseFactory()
        self.admin = ViewsAdminProfileFactory().user
        self.client.login(username=self.admin.username, password="Admin")

    def test_get_teams(self):
        ''' Any teams in the course will be returned via GET '''
        response = self.client.get('/admin_team/' + str(self.crs.pk) + '/',
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''No teams have been added so test
        response.data - should be empty'''
        self.assertEqual(response.data, [])

    def test_create_team(self):
        ''' Teams created via POST '''
        response = self.client.post('/admin_team/' + str(self.crs.pk) + '/',
                                    {'team_name': 'Test Team Name'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        '''After team is created, it should return the team data
        in response.data'''
        # The student id should not be hard coded - manually look up?
        self.assertEqual(response.data, {'id': 4,
                                         'username': u'Test Team Name_1',
                                         'first_name': u'Test Team Name'})

    def test_create_then_update_team(self):
        pass

    def test_create_update_delete_team(self):
        ''' Any students in the course will be returned via GET '''
        response = self.client.post('/admin_team/' + str(self.crs.pk) + '/',
                                    {'team_name': 'Test Team Name'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': 4,
                                         'username': u'Test Team Name_1',
                                         'first_name': u'Test Team Name'})
        response = self.client.delete('/admin_team/' + str(self.crs.pk) + '/',
                                      format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

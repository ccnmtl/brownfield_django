from django.test import TestCase, RequestFactory
from django.test.client import Client

from factories import UserProfileFactory, UserFactory, \
    CourseFactory, TeamFactory, DocumentFactory

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient


class TestAdminViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.profile = UserProfileFactory(
            user=UserFactory(username='admin'), profile_type='AD')
        self.client.login(username=self.profile.user.username, password='test')

    def test_home(self):
        request = self.client.get("/ccnmtl/home/" +
                                  str(self.profile.pk) + '/')
        self.assertTemplateUsed(request,
                                'main/ccnmtl/home_dash/ccnmtl_home.html')

    def test_get_course_details(self):
        '''
        Requesting the course details page should redirect
        the admin to a course dashboard where they can create
        teams and students, and put students in teams.
        '''
        self.course = CourseFactory(professor=self.profile.user)
        request = self.client.get("/course_details/" +
                                  str(self.course.pk) + '/')
        self.assertTemplateUsed(request,
                                'main/ccnmtl/course_dash/course_home.html')


class TestCourseRestViews(APITestCase):
    '''Test course related urls'''
 
    def setUp(self):
        '''Courses ordered by name... setting now'''
        self.client = APIClient()
        self.admin = UserProfileFactory(user=UserFactory(username='admin'),
                                        profile_type='AD')
        self.teacher = UserProfileFactory(user=UserFactory(username='teacher'),
                                          profile_type='TE')
        self.admin_crs = CourseFactory(professor=self.admin.user,
                                       name='ACourse')
        self.teacher_crs = CourseFactory(professor=self.teacher.user,
                                         name='BCourse')
        self.random_crs1 = CourseFactory(
            professor=UserFactory(username='someuser'), name='CCourse')
        self.random_crs2 = CourseFactory(
            professor=UserFactory(username='someotheruser'), name='DCourse')
 
    def test_get_courses_as_admin(self):
        ''' Get all Courses. '''
        self.client.login(username=self.admin.user.username, password="test")
        
        response = self.client.get('/api/course/',
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]['name'], self.admin_crs.name)
        self.assertEqual(response.data[1]['name'], self.teacher_crs.name)
        self.assertEqual(response.data[2]['name'], self.random_crs1.name)
        self.assertEqual(response.data[3]['name'], self.random_crs2.name)
 
    def test_get_courses_as_teacher(self):
        ''' Get teachers courses. '''
        self.client.login(username=self.teacher.user.username, password="test")
        response = self.client.get('/api/course/',
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.teacher_crs.name)


class TestUserViewset(APITestCase):
    '''Test user viewset class, currently only admins should be returned
    as list of all users, everyone else should be returned their own user,
    if they are returned anything at all'''
 
    def setUp(self):
        '''users ordered by username'''
        self.client = APIClient()
        self.admin = UserProfileFactory(user=UserFactory(username='admin'),
                                        profile_type='AD')
        self.teacher = UserProfileFactory(user=UserFactory(username='teacher'),
                                          profile_type='TE')
        self.user_one = UserFactory(username='auser')
        self.user_two = UserFactory(username='buser')
        self.user_three = UserFactory(username='cuser')

    def test_get_users_as_admin(self):
        ''' User is admin, should return list of all users '''
        self.client.login(username=self.admin.user.username, password="test")
        response = self.client.get('/api/user/',
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]['username'],
                         self.admin.user.username)
        self.assertEqual(response.data[1]['username'], self.user_one.username)
        self.assertEqual(response.data[2]['username'], self.user_two.username)
        self.assertEqual(response.data[3]['username'],
                         self.user_three.username)
        self.assertEqual(response.data[4]['username'],
                         self.teacher.user.username)
 
 
class TestDocumentRestViews(APITestCase):
    '''Test document related urls'''
 
    def setUp(self):
        self.client = APIClient()
        self.admin = UserProfileFactory(user=UserFactory(username='admin'),
                                        profile_type='AD')
        self.teacher = UserProfileFactory(user=UserFactory(username='teacher'),
                                          profile_type='TE')
        self.course = CourseFactory(professor=self.teacher.user,
                                    name='TestCourse')

    def test_get_documents(self):
        ''' Get all Course Documents. '''
        self.client.login(username=self.teacher.user.username, password="test")
        response = self.client.get('/api/document/?course=' + str(self.course.pk),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''By default courses have 8 documents'''
        self.assertEqual(len(response.data), 8)
 
    def test_release_revoke_document(self):
        ''' Release a document. '''
        self.client.login(username=self.teacher.user.username, password="test")
        response = self.client.get('/api/document/?course=' + str(self.course.pk),
                                   format='json')
        response = self.client.put(
            '/api/document/' + str(response.data[0]['id']) + '/',
            {'id': response.data[0]['id'], 'name': response.data[0]['name'],
             'link': response.data[0]['link'],
             'visible': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, True)
#         response = self.client.put(
#             '/api/document/' + str(doc.pk) + '/', format='json')
#         self.assertEqual(response.data, False)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
 
 
# class TestStudentRestViews(APITestCase):
#     '''Test student related urls and methods, has GET, PUT/update,
#     POST/create, DELETE/destroy'''
# 
#     def setUp(self):
#         ''' Admin will log in, and navigate to a course page. '''
#         self.client = APIClient()
#         self.factory = APIRequestFactory()
#         self.crs = AdminUserCourseFactory()
#         self.admin = ViewsAdminProfileFactory().user
#         self.client.login(username=self.admin.username, password="Admin")
# 
#     def test_get_students(self):
#         ''' Any students in the course will be returned via GET '''
#         response = self.client.get('/api/student/?course=' +
#                                    str(self.crs.pk), format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         '''No students have been added so test
#         response.data - should be empty'''
#         self.assertEqual(response.data, [])
# 
#     def test_create_student(self):
#         ''' Any students in the course will be returned via GET '''
#         response = self.client.post('/api/student/?course=' + str(self.crs.pk),
#                                     {'first_name': 'Student First Name',
#                                      'last_name': 'Student Last Name',
#                                      'email': 'studentemail@email.com'},
#                                     format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         '''After student is created, it should return the student data
#         in response.data'''
#         # The student id should not be hard coded - manually look up?
#         self.assertEqual(response.data, {'id': 4,
#                                          'first_name': u'Student First Name',
#                                          'last_name': u'Student Last Name',
#                                          'email': u'studentemail@email.com'})
# 
#     def test_create_then_update_student(self):
#         ''' Any students in the course will be returned via GET '''
#         response = self.client.post('/api/student/?course=' + str(self.crs.pk),
#                                     {'first_name': 'Student First Name',
#                                      'last_name': 'Student Last Name',
#                                      'email': 'studentemail@email.com'},
#                                     format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         '''After student is created, it should return the student data
#         in response.data'''
#         self.assertEqual(response.data, {'id': 4,
#                                          'first_name': u'Student First Name',
#                                          'last_name': u'Student Last Name',
#                                          'email': u'studentemail@email.com'})
#         # need to update view possibly to return student data, although it
#         # seems backbone doesn't need it, it is probably good for testing
#         # and diagnostics, also change wrong status codes
#         response = self.client.put('/api/student/4/',
#                                    {'first_name': 'Edit First Name',
#                                     'last_name': 'Edit Last Name',
#                                     'email': 'editmail@email.com'},
#                                    format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
# 
#     def test_create_update_delete_student(self):
#         ''' Any students in the course will be returned via GET '''
#         response = self.client.post('/api/student/?course=' + str(self.crs.pk),
#                                     {'first_name': 'Student First Name',
#                                      'last_name': 'Student Last Name',
#                                      'email': 'studentemail@email.com'},
#                                     format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         '''After student is created, it should return the student data
#         in response.data'''
#         self.assertEqual(response.data, {'id': 4,
#                                          'first_name': u'Student First Name',
#                                          'last_name': u'Student Last Name',
#                                          'email': u'studentemail@email.com'})
#         response = self.client.put('/api/student/4/',
#                                    {'first_name': 'Edit First Name',
#                                     'last_name': 'Edit Last Name',
#                                     'email': 'editmail@email.com'},
#                                    format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         response = self.client.delete('/api/student/4/', format='json')
#         # is there as success code for delete?
#         # should I test the models to see if they were deleted as well?
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
# 
# 
# class TestTeamRestViews(APITestCase):
#     '''Test team related urls and methods, has GET, PUT/update,
#     POST/create, DELETE/destroy'''
# 
#     def setUp(self):
#         ''' Admin will log in, and navigate to a course page. '''
#         self.client = APIClient()
#         self.factory = APIRequestFactory()
#         self.crs = AdminUserCourseFactory()
#         self.admin = ViewsAdminProfileFactory().user
#         self.client.login(username=self.admin.username, password="Admin")
# 
#     def test_get_teams(self):
#         ''' Any teams in the course will be returned via GET '''
#         response = self.client.get('/admin_team/' + str(self.crs.pk) + '/',
#                                    format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         '''No teams have been added so test
#         response.data - should be empty'''
#         self.assertEqual(response.data, [])
# 
#     def test_create_team(self):
#         ''' Teams created via POST '''
#         response = self.client.post('/admin_team/' + str(self.crs.pk) + '/',
#                                     {'team_name': 'Test Team Name'},
#                                     format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         '''After team is created, it should return the team data
#         in response.data'''
#         # The student id should not be hard coded - manually look up?
#         self.assertEqual(response.data, {'id': 4,
#                                          'username': u'Test Team Name_1',
#                                          'first_name': u'Test Team Name'})
# 
#     def test_create_then_update_team(self):
#         pass
# 
#     def test_create_update_delete_team(self):
#         ''' Any students in the course will be returned via GET '''
#         response = self.client.post('/admin_team/' + str(self.crs.pk) + '/',
#                                     {'team_name': 'Test Team Name'},
#                                     format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data, {'id': 4,
#                                          'username': u'Test Team Name_1',
#                                          'first_name': u'Test Team Name'})
#         response = self.client.delete('/admin_team/' + str(self.crs.pk) + '/',
#                                       format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

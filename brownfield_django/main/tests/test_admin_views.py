from django.core import mail
from django.test import TestCase
from django.test.client import Client

from factories import UserProfileFactory, UserFactory, \
    CourseFactory, TeamFactory

from rest_framework import status
from rest_framework.test import APITestCase
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

    def test_get_documents_as_teacher(self):
        ''' Get all Course Documents. '''
        self.client.login(username=self.teacher.user.username, password="test")
        response = self.client.get(
            '/api/document/?course=' + str(self.course.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''By default courses have 8 documents'''
        self.assertEqual(len(response.data), 8)

    def test_release_document_as_teacher(self):
        ''' Release a document. '''
        self.client.login(username=self.teacher.user.username, password="test")
        response = self.client.get('/api/document/?course=' +
                                   str(self.course.pk),
                                   format='json')
        new_response = self.client.put(
            '/api/document/' + str(response.data[0]['id']) + '/',
            {'id': response.data[0]['id'], 'name': response.data[0]['name'],
             'link': response.data[0]['link'],
             'visible': True}, format='json')
        self.assertEqual(new_response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_response.data['visible'], True)
        third_response = self.client.put(
            '/api/document/' + str(response.data[0]['id']) + '/',
            {'id': response.data[0]['id'], 'name': response.data[0]['name'],
             'link': response.data[0]['link'],
             'visible': False}, format='json')
        self.assertEqual(third_response.status_code, status.HTTP_200_OK)
        self.assertEqual(third_response.data['visible'], False)

    def test_get_documents_as_admin(self):
        ''' Get all Course Documents. '''
        self.client.login(username=self.admin.user.username, password="test")
        response = self.client.get(
            '/api/document/?course=' + str(self.course.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''By default courses have 8 documents'''
        self.assertEqual(len(response.data), 8)

    def test_release_document_as_admin(self):
        ''' Release a document. '''
        self.client.login(username=self.admin.user.username, password="test")
        response = self.client.get('/api/document/?course=' +
                                   str(self.course.pk),
                                   format='json')
        new_response = self.client.put(
            '/api/document/' + str(response.data[0]['id']) + '/',
            {'id': response.data[0]['id'], 'name': response.data[0]['name'],
             'link': response.data[0]['link'],
             'visible': True}, format='json')
        self.assertEqual(new_response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_response.data['visible'], True)
        third_response = self.client.put(
            '/api/document/' + str(response.data[0]['id']) + '/',
            {'id': response.data[0]['id'], 'name': response.data[0]['name'],
             'link': response.data[0]['link'],
             'visible': False}, format='json')
        self.assertEqual(third_response.status_code, status.HTTP_200_OK)
        self.assertEqual(third_response.data['visible'], False)


class TestStudentRestViews(APITestCase):
    '''Test student related urls and methods, has GET, PUT/update,
    POST/create, DELETE/destroy'''

    def setUp(self):
        ''' Admin will log in, and navigate to a course page. '''
        self.client = APIClient()
        self.admin = UserProfileFactory(user=UserFactory(username='admin'),
                                        profile_type='AD')
        self.teacher = UserProfileFactory(user=UserFactory(username='teacher'),
                                          profile_type='TE')
        self.course = CourseFactory(professor=self.teacher.user,
                                    name='TestCourse')
        self.populated_course = CourseFactory(professor=self.teacher.user,
                                              name='TestCourse')
        self.student_one = UserProfileFactory(
            user=UserFactory(
                username='student_one', first_name='astudent',
                last_name='student_one', email='student_one@email.com'),
            profile_type='ST', course=self.populated_course)
        self.student_two = UserProfileFactory(
            user=UserFactory(
                username='student_two', first_name='bstudent',
                last_name='student_two', email='student_two@email.com'),
            profile_type='ST', course=self.populated_course)
        self.student_three = UserProfileFactory(
            user=UserFactory(
                username='student_three', first_name='cstudent',
                last_name='student_three', email='student_three@email.com'),
            profile_type='ST', course=self.populated_course)
        self.student_four = UserProfileFactory(
            user=UserFactory(
                username='student_four', first_name='dstudent',
                last_name='student_four', email='student_four@email.com'),
            profile_type='ST', course=self.populated_course)

    def test_get_students_as_teacher(self):
        ''' Any students in the course will be returned via GET '''
        self.client.login(username=self.teacher.user.username, password="test")
        response = self.client.get('/api/student/?course=' +
                                   str(self.course.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''No students have been added so test
        response.data - should be empty'''
        self.assertEqual(response.data, [])

    def test_get_students_as_admin(self):
        ''' Any students in the course will be returned via GET '''
        self.client.login(username=self.admin.user.username, password="test")
        response = self.client.get('/api/student/?course=' +
                                   str(self.course.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''No students have been added so test
        response.data - should be empty'''
        self.assertEqual(response.data, [])

    def test_create_student_as_admin(self):
        ''' Testing that admin can create students for teacher's course.  '''
        self.client.login(username=self.admin.user.username, password="test")
        response = self.client.post(
            '/api/student/?course=' + str(self.course.pk),
            {'first_name': 'Sam',
             'last_name': 'Smith',
             'email': 'studentemail@email.com'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        '''After student is created, it should return the student data
        in response.data'''
        self.assertEqual(response.data, {'id': response.data['id'],
                                         'first_name': u'Sam',
                                         'last_name': u'Smith',
                                         'email': u'studentemail@email.com'})

    def test_create_student_as_teacher(self):
        ''' Testing that admin can create students for teacher's course.  '''
        self.client.login(username=self.teacher.user.username, password="test")
        response = self.client.post(
            '/api/student/?course=' + str(self.course.pk),
            {'first_name': 'Sam',
             'last_name': 'Smith',
             'email': 'studentemail@email.com'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        '''After student is created, it should return the student data
        in response.data'''
        self.assertEqual(response.data, {'id': response.data['id'],
                                         'first_name': u'Sam',
                                         'last_name': u'Smith',
                                         'email': u'studentemail@email.com'})

    def test_get_students_as_teacher_class(self):
        ''' Now trying get on populated course. '''
        self.client.login(username=self.teacher.user.username, password="test")
        response = self.client.get(
            '/api/student/?course=' +
            str(self.populated_course.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''QuerySset is ordered by first name'''
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]['first_name'],
                         self.student_one.user.first_name)
        self.assertEqual(response.data[1]['first_name'],
                         self.student_two.user.first_name)
        self.assertEqual(response.data[2]['first_name'],
                         self.student_three.user.first_name)
        self.assertEqual(response.data[3]['first_name'],
                         self.student_four.user.first_name)

    def test_get_students_as_admin_class(self):
        ''' Now trying get on populated course. '''
        self.client.login(username=self.admin.user.username, password="test")
        response = self.client.get('/api/student/?course=' +
                                   str(self.populated_course.pk),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        '''QuerySset is ordered by first name'''
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]['first_name'],
                         self.student_one.user.first_name)
        self.assertEqual(response.data[1]['first_name'],
                         self.student_two.user.first_name)
        self.assertEqual(response.data[2]['first_name'],
                         self.student_three.user.first_name)
        self.assertEqual(response.data[3]['first_name'],
                         self.student_four.user.first_name)

    def test_update_student_as_admin(self):
        ''' Edit a student as admin '''
        self.client.login(username=self.admin.user.username, password="test")
        response = self.client.get('/api/student/?course=' +
                                   str(self.populated_course.pk),
                                   format='json')
        new_response = self.client.put(
            '/api/student/' + str(response.data[0]['id']) + '/',
            {'first_name': 'Edit First Name',
             'last_name': 'Edit Last Name',
             'email': 'editmail@email.com'},
            format='json')
        self.assertEqual(new_response.status_code, status.HTTP_200_OK)

    def test_update_student_as_teacher(self):
        ''' Edit a student as teacher '''
        self.client.login(username=self.teacher.user.username, password="test")
        response = self.client.get('/api/student/?course=' +
                                   str(self.populated_course.pk),
                                   format='json')
        new_response = self.client.put(
            '/api/student/'+str(response.data[0]['id']) + '/',
            {'first_name': 'Edit First Name',
             'last_name': 'Edit Last Name',
             'email': 'editmail@email.com'},
            format='json')
        self.assertEqual(new_response.status_code, status.HTTP_200_OK)

    def test_delete_student_as_admin(self):
        ''' Delete student as admin '''
        self.client.login(username=self.admin.user.username, password="test")
        response = self.client.get('/api/student/?course=' +
                                   str(self.populated_course.pk),
                                   format='json')
        new_response = self.client.delete('/api/student/' +
                                          str(response.data[0]['id']) +
                                          '/', format='json')
        self.assertEqual(new_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_student_as_teacher(self):
        ''' Delete student as teacher '''
        self.client.login(username=self.teacher.user.username, password="test")
        response = self.client.get('/api/student/?course=' +
                                   str(self.populated_course.pk),
                                   format='json')
        new_response = self.client.delete('/api/student/' +
                                          str(response.data[0]['id']) +
                                          '/', format='json')
        self.assertEqual(new_response.status_code, status.HTTP_204_NO_CONTENT)


class TestTeamRestViews(APITestCase):
    '''Test team related urls and methods, has GET, PUT/update,
    POST/create, DELETE/destroy'''

    def setUp(self):
        ''' Test that teachers and admins can view and add teams. Team
        nare '''
        self.client = APIClient()
        self.admin = UserProfileFactory(user=UserFactory(username='admin'),
                                        profile_type='AD')
        self.teacher = UserProfileFactory(user=UserFactory(username='teacher'),
                                          profile_type='TE')
        self.course = CourseFactory(professor=self.teacher.user,
                                    name='TestCourse')

    def test_teacher_get_create_delete_teams(self):
        ''' Any teams in the course will be returned via GET '''
        self.client.login(username=self.teacher.user.username, password="test")
        response = self.client.get('/api/eteam/?course=' +
                                   str(self.course.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ''' No teams have been added so test response.data should be empty '''
        self.assertEqual(response.data, [])
        ''' Test that teacher can create students for teacher's course. '''
        self.client.login(username=self.teacher.user.username, password="test")
        new_response = self.client.post(
            '/api/eteam/?course=' + str(self.course.pk),
            {'team_name': 'SomeTeam'}, format='json')
        self.assertEqual(new_response.status_code, status.HTTP_201_CREATED)
        ''' After team is created, it should return the team's data,
        which consists of 3 attributes - the teams given name, teams auto-
        generated name, and the team id '''
        self.assertEqual(len(new_response.data), 3)
        self.assertEqual(new_response.data['first_name'], u'SomeTeam')
        ''' Delete team as teacher '''
        another_response = self.client.delete('/api/eteam/' +
                                              str(new_response.data['id']) +
                                              '/', format='json')
        self.assertEqual(another_response.status_code,
                         status.HTTP_204_NO_CONTENT)

    def test_admin_get_create_delete_teams(self):
        ''' Any teams in the course will be returned via GET '''
        self.client.login(username=self.admin.user.username, password="test")
        response = self.client.get('/api/eteam/?course=' +
                                   str(self.course.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ''' No teams have been added so test response.data should be empty'''
        self.assertEqual(response.data, [])
        ''' Testing that admin can create teams for a course. '''
        new_response = self.client.post(
            '/api/eteam/?course=' + str(self.course.pk),
            {'team_name': 'SomeTeam'}, format='json')
        self.assertEqual(new_response.status_code, status.HTTP_201_CREATED)
        ''' After team is created, it should return the team's data,
        which is 3 attributes '''
        self.assertEqual(len(new_response.data), 3)
        self.assertEqual(new_response.data['first_name'], u'SomeTeam')
        ''' Delete team as admin '''
        another_response = self.client.delete('/api/eteam/' +
                                              str(new_response.data['id']) +
                                              '/', format='json')
        self.assertEqual(another_response.status_code,
                         status.HTTP_204_NO_CONTENT)

    def test_admin_create_teams_long_teamname(self):
        self.client.login(username=self.admin.user.username, password="test")
        new_response = self.client.post(
            '/api/eteam/?course=' + str(self.course.pk),
            {
                'team_name': 'Some really really long team name'
            },
            format='json')
        self.assertEqual(new_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(new_response.data), 3)
        self.assertEqual(new_response.data['first_name'],
                         u'Some really really long team n')


class TestNotifyStudentsView(TestCase):

    def setUp(self):
        ''' Teacher has created a course with students and teams,
        and now wishes to activate the course/notify students. This view
        should email all of the students in the course notifying them of which
        team they are in and how to log in to the site.'''
        self.client = Client()
        self.teacher = UserProfileFactory(user=UserFactory(username='teacher'),
                                          profile_type='TE')
        self.admin = UserProfileFactory(user=UserFactory(username='admin'),
                                        profile_type='AD')
        self.course = CourseFactory(professor=self.admin.user,
                                    name='TestCourse')
        self.team_one = TeamFactory(
            user=UserFactory(
                username='uniq_team_one', first_name='TeamOne'),
            team_passwd="Test_Team", course=self.course)
        self.team_two = TeamFactory(
            user=UserFactory(
                username='uniq_team_two', first_name='TeamTwo'),
            team_passwd="Test_Team", course=self.course)
        self.student_one = UserProfileFactory(
            user=UserFactory(
                username='student_one', first_name='astudent',
                last_name='student_one', email='student_one@email.com'),
            profile_type='ST', course=self.course)
        self.student_two = UserProfileFactory(
            user=UserFactory(
                username='student_two', first_name='bstudent',
                last_name='student_two', email='student_two@email.com'),
            profile_type='ST', course=self.course)
        self.student_three = UserProfileFactory(
            user=UserFactory(
                username='student_three', first_name='cstudent',
                last_name='student_three', email='student_three@email.com'),
            profile_type='ST', course=self.course)
        self.student_four = UserProfileFactory(
            user=UserFactory(
                username='student_four', first_name='dstudent',
                last_name='student_four', email='student_four@email.com'),
            profile_type='ST', course=self.course)

    def test_emails_sent_to_students(self):
        ''' Post the table of students and teams, make sure the view
        sends an email for each student '''
        self.client.login(username=self.admin.user.username, password="test")
        response = self.client.post(
            '/activate_course/' + str(self.course.pk) + '/',
            {u'student_list': [u'[{ "student": {"pk":"' +
             str(self.student_one.user.pk) + '"' +
             ',"first_name":"' + str(self.student_one.user.first_name) + '"' +
             ',"last_name":"' + str(self.student_one.user.last_name) + '"' +
             ',"email":"' + str(self.student_one.user.email) + '"' +
             ',"team_id":"' + str(self.team_one.pk) + '"' +
             ',"team_name":"' + str(self.team_one.user.username) + '"}},{' +
             '"student": {"pk":"' + str(self.student_two.user.pk) + '"' +
             ',"first_name":"' + str(self.student_two.user.first_name) + '"' +
             ',"last_name":"' + str(self.student_two.user.last_name) + '"' +
             ',"email":"' + str(self.student_two.user.email) + '"' +
             ',"team_id":"' + str(self.team_one.pk) + '"' +
             ',"team_name":"' + str(self.team_one.user.username) + '"}},{' +
             '"student": {"pk":"' + str(self.student_three.user.pk) + '"' +
             ',"first_name":"' + str(self.student_three.user.first_name) +
             '"' + ',"last_name":"' + str(self.student_three.user.last_name) +
             '"' + ',"email":"' + str(self.student_three.user.email) + '"' +
             ',"team_id":"' + str(self.team_two.pk) + '"' +
             ',"team_name":"' + str(self.team_two.user.username) + '"}},{' +
             '"student": {"pk":"' + str(self.student_four.user.pk) + '"' +
             ',"first_name":"' + str(self.student_four.user.first_name) +
             '"' + ',"last_name":"' + str(self.student_four.user.last_name) +
             '"' + ',"email":"' + str(self.student_four.user.email) + '"' +
             ',"team_id":"' + str(self.team_two.pk) + '"' +
             ',"team_name":"' + str(self.team_two.user.username) + '"}}]']},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 4)
        self.assertEqual(mail.outbox[0].subject, "Welcome to Brownfield!")

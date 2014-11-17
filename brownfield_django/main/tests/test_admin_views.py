import json
# from datetime import datetime

from django.test import TestCase, RequestFactory
from django.test.client import Client
# from django.contrib.auth.models import User
from factories import ViewsAdminProfileFactory, AdminUserCourseFactory, AdminUserDocumentFactory

# from brownfield_django.main.views import CourseViewSet
# DetailJSONCourseView
# from django.core.urlresolvers import reverse
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
        response = self.client.get('/api/document/?course=' + str(crs.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_release_revoke_document(self):
        ''' Release a document. '''
        crs = AdminUserCourseFactory()
        doc = crs.document_set.all()[0]
        response = self.client.put(
            '/api/document/' + str(doc.pk) + '/', {'id': doc.pk, 'name': u'Test Document for Admin',
             'link': u"<a href='/path/to/the/course/document/here'></a>",
             'visible': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, True)
        response = self.client.put(
             '/api/document/' + str(doc.pk) + '/', format='json')
        self.assertEqual(response.data, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_update_course(self):
        '''
        Calling get for a update course should return the details of
        the course to the page edit form so that the edit form is already
        filled out.
        '''
        self.admin_course = AdminUserCourseFactory()
        response = self.client.get('/update_course/' + str(self.admin_course.pk),
                                   {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        the_json = json.loads(response.content)
        self.assertTrue('course' in the_json)#'enableNarrative' in the_json)#the_json['enableNarrative'])#, True)
#         self.assertTrue(the_json['course']['active'], True)
#         self.assertTrue(the_json['name'], "Test Course")
#         self.assertTrue(the_json['startingBudget'], 100000)
#         self.assertTrue(the_json['message'], "Hello you non existent students.")

#    professor = factory.SubFactory(UserFactory)
#     def test_login_post_ajax(self):
#         response = self.client.post('/accounts/login/',
#                                     {'username': '',
#                                       'password': ''},
#                                     HTTP_X_REQUESTED_WITH='XMLHttpRequest')
#  158         self.assertEquals(response.status_code, 200)
#  159         the_json = json.loads(response.content)
#  160         self.assertTrue(the_json['error'], True)
#  161 
#  162         response = self.client.post('/accounts/login/',
#  163                                     {'username': self.user.username,
#  164                                      'password': 'test'},
#  165                                     HTTP_X_REQUESTED_WITH='XMLHttpRequest')
#  166         self.assertEquals(response.status_code, 200)
#  167         the_json = json.loads(response.content)
#  168         self.assertTrue(the_json['next'], "/")
#  169         self.assertTrue('error' not in the_json)

#         self.admin_course = AdminUserCourseFactory()
# 
#         request = RequestFactory().get('/update_course/' +
#                                        str(self.admin_course.pk))
#         request.user = self.admin
#         view = DetailJSONCourseView()
#         view.request = request

#         view.object = request.user.profile
#         ctx = view.get_context_data()
#
#         admin_group = SchoolGroupFactory(creator=self.admin,
#                                          school=self.admin.profile.school)
#         teacher_group = SchoolGroupFactory(creator=self.teacher,
#                                         school=self.teacher.profile.school)
#
#         # archived groups
#         SchoolGroupFactory(creator=self.teacher,
#                            school=self.teacher.profile.school,
#                            archived=True)
#         SchoolGroupFactory(creator=self.admin,
#                            school=self.admin.profile.school,
#                            archived=True)
#
#         # alt_creator/alt school
#         SchoolGroupFactory(creator=TeacherProfileFactory().user)
#
#         self.assertEquals(ctx['optionb'], self.hierarchy)
#         self.assertIsNotNone(ctx['profile_form'])
#         self.assertEquals(ctx['countries'], COUNTRY_CHOICES)
#         self.assertEquals(ctx['joined_groups'].count(), 0)
#         self.assertEquals(len(ctx['managed_groups']), 2)
#         self.assertEquals(ctx['managed_groups'][0], admin_group)
#         self.assertEquals(ctx['managed_groups'][1], teacher_group)


        # self.assertEqual(response.status_code, 200)
#         the_json = json.loads(response.content)
#         self.assertEqual(
#             the_json,
#             {'course': [{'id': str(self.admin_course.id),
#              'name': self.admin_course.name,
#              'startingBudget': self.admin_course.startingBudget,
#              'enableNarrative': self.admin_course.enableNarrative,
#              'message': self.admin_course.message,
#              'active': self.admin_course.active,
#              'archive': self.admin_course.archive,
#              'professor': str(self.admin_course.professor)
#              }]})
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_post_update_course(self):
#         '''
#         Calling post on update_course should update the course,
#         and return the details to the page.
#         '''
#         self.admin_course = AdminUserCourseFactory()
#         response = self.client.post("/update_course/" +
#                                    str(self.admin_course.pk),
#                                    format='json')
#         the_json = json.loads(response.content)
#         self.assertEqual(
#             the_json,
#             {'course': [{'id': str(self.admin_course.id),
#              'name': self.admin_course.name,
#              'startingBudget': self.admin_course.startingBudget,
#              'enableNarrative': self.admin_course.enableNarrative,
#              'message': self.admin_course.message,
#              'active': self.admin_course.active,
#              'archive': self.admin_course.archive,
#              'professor': str(self.admin_course.professor)
#              }]})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# class TestAdminRESTViews(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.factory = APIRequestFactory()
#         self.admin = ViewsAdminProfileFactory().user
#         self.client.login(username=self.admin.username, password="Admin")

#     def test_get_all_courses(self):
#         view = CourseViewSet.as_view()
#         request = self.factory.get('/api/course/')
#         response = view(request)

#     def test_get_user_courses(self):
#         view = CourseViewSet.as_view()
#         request = self.ajax_factory.post('/api/course/',
#                                     {'name': 'new_course_name'},
#                                     format='json')
#         response = view(request)

#     def test_add_course_by_name(self):
#         view = CourseViewSet.as_view()
#         request = self.factory.post('/api/course/',
#                                     json.dumps({'name': 'new_course_name'}),
#                                     format='json')
#         response = view(request)
        #self.assertEqual(response.data, {'name': 'new_course_name'})
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_get_user_courses(self):
#         '''
#         Return list of user created courses - just
#         those the admin user created.
#         '''
#         pass
#         crs = AdminUserCourseFactory()
#         c1 = CourseOneFactory()
#         c2 = CourseTwoFactory()
#         c3 = CourseThreeFactory()
#         response = self.client.get('/user_courses/', format='json')
#         self.assertEqual(response.data, [{'id': crs.pk,
#                                          'name': u'Test Course'}])
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_all_courses(self):
#         '''
#         Return list of courses - those the admin user
#         created and all others.
#         '''
#         pass
#         c1 = CourseOneFactory()
#         c2 = CourseTwoFactory()
#         c3 = CourseThreeFactory()
#         response = self.client.get('/all_courses/', format='json')
#         '''KEEPS RETURNING TEST COURSE NO IDEA WHY - THERE
#         ARE ONLY 3 FACTORIES HERE'''
#         self.assertEqual(
#             response.data,
#             [{'name': u'Test Course', 'id': c1.pk},
#              {'name': u'Test Course One', 'id': c1.pk},
#              {'name': u'Test Course Two', 'id': c2.pk},
#              {'name': u'Test Course Three', 'id': c3.pk}])
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


#     def test_remove_course(self):
#         '''
#         Calling get for a course should redirect the instructor to a
#         course detail page where they can create teams, add students,
#         and put students in teams.
#         '''
#         pass
#         c1 = CourseOneFactory()
#         c2 = CourseTwoFactory()
#         c3 = CourseThreeFactory()
#         response = self.client.delete('/course/' + str(c1.pk), format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#    '''Test student related urls'''
#     def test_create_student(self):
#         '''
#         Calling post with desired name of the new course
#         should result in a new course with that name being created
#         and the course info (key) being returned to the browser to update
#         the course list.
#         '''
#         pass

#     def test_get_students(self):
#         '''
#         Calling get for a course should redirect the instructor to a
#         course detail page where they can create teams, add students,
#         and put students in teams.
#         '''
#         pass

#     def test_update_student(self):
#         '''
#         Calling get for a course should redirect the instructor to a
#         course detail page where they can create teams, add students,
#         and put students in teams.
#         '''
#         pass

#     def test_remove_student(self):
#         '''
#         Calling get for a course should redirect the instructor to a
#         course detail page where they can create teams, add students,
#         and put students in teams.
#         '''
#         pass

#     '''Test team related urls'''

#     def test_post_team(self):
#         '''
#         Calling post with desired name of the new course
#         should result in a new course with that name being created
#         and the course info (key) being returned to the browser to update
#         the course list.
#         '''
#         pass

#     def test_get_team(self):
#         '''
#         Calling get for a course should redirect the instructor to a
#         course detail page where they can create teams, add students,
#         and put students in teams.
#         '''
#         pass

#     def test_update_team(self):
#         '''
#         Calling get for a course should redirect the instructor to a
#         course detail page where they can create teams, add students,
#         and put students in teams.
#         '''
#         pass

#     def teamtest_remove_course(self):
#         '''
#         Calling get for a course should redirect the instructor to a
#         course detail page where they can create teams, add students,
#         and put students in teams.
#         '''
#         pass

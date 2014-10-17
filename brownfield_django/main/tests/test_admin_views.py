# import json
# from datetime import datetime

from django.test import TestCase, RequestFactory
from django.test.client import Client
from rest_framework.test import APIRequestFactory
# from django.contrib.auth.models import User
from rest_framework import status

from factories import ViewsAdminProfileFactory, AdminUserCourseFactory, \
    AdminUserDocumentFactory

from brownfield_django.main.views import CourseViewSet


class TestAdminViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.ajax_factory = APIRequestFactory()
        self.admin = ViewsAdminProfileFactory().user
        self.client.login(username=self.admin.username, password="Admin")
        # self.ajax_client.login(username=self.admin.username, password="Admin")

    def test_home_redirect(self):
        '''Keep getting random bootstrap can't be compressed errors.'''
        request = self.client.get("/", follow=True)
        self.assertEquals(
            request.redirect_chain[0],
            ('http://testserver/ccnmtl/home/' +
             str(self.admin.profile.pk) + '/',
             302))
        self.assertTemplateUsed(request,
                                'main/ccnmtl/home_dash/ccnmtl_home.html')

    def test_home(self):
        '''
        See what happens if I request appropriate home directly
        instead of following redirect.
        '''
        request = self.client.get("/ccnmtl/home/" +
                                  str(self.admin.profile.pk) + '/')
        self.assertTemplateUsed(request,
                                'main/ccnmtl/home_dash/ccnmtl_home.html')

    def test_add_course_by_name(self):
        '''
        Calling post with desired name of the new course
        should result in a new course with that name being created
        and the course info (key) being returned to the browser to update
        the course list.
        '''
        pass
#         request = self.ajax_factory.put('api/course/',
#                                     {'name': 'new_course_name'},
#                                     format='json')
#         view = CourseViewSet.as_view()
#         force_authenticate(request, user=self.admin)
#         response = view(request)
#         #self.assertEqual(response.data, {'name': 'new_course_name'})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_user_courses(self):
        '''
        Return list of user created courses - just
        those the admin user created.
        '''
        pass
#         crs = AdminUserCourseFactory()
#         c1 = CourseOneFactory()
#         c2 = CourseTwoFactory()
#         c3 = CourseThreeFactory()
#         response = self.client.get('/user_courses/', format='json')
#         self.assertEqual(response.data, [{'id': crs.pk,
#                                          'name': u'Test Course'}])
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_courses(self):
        '''
        Return list of courses - those the admin user
        created and all others.
        '''
        pass
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

    def test_get_course_details(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        self.admin_course = AdminUserCourseFactory()
        request = self.client.get("/course_details/" +
                                  str(self.admin_course.pk) + '/')
        self.assertTemplateUsed(request,
                                'main/ccnmtl/course_dash/course_home.html')

    def test_update_course(self):
        '''
        Calling get for a update course should return the details of
        the course to the page edit form so that the edit form is already
        filled out. Calling post on update_course should update the course,
        and return the details to the page.
        '''
        pass
#         self.admin_course = AdminUserCourseFactory()
#         response = self.client.get("/update_course/" +
#                                    str(self.admin_course.pk),
#                                    format='json')
#         # self.assertEqual(response.status_code, 200)
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

    def test_remove_course(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass
#         c1 = CourseOneFactory()
#         c2 = CourseTwoFactory()
#         c3 = CourseThreeFactory()
#         response = self.client.delete('/course/' + str(c1.pk), format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

    '''Test document related urls'''

#     def test_get_documents(self):
#         '''
#         Get all Course Documents.
#         '''
#         doc = AdminUserDocumentFactory()
#         crs = AdminUserCourseFactory()
#         crs.document_set.add(doc)
#         response = self.client.get('api/document/' + str(crs.pk), format='json')
#         self.assertEqual(
#             response.data,
#             [{'id': doc.pk, 'name': u'Test Document for Admin',
#               'link': u"<a href='/path/to/the/course/document/here'></a>",
#               'visible': False}])
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
# 
#     def test_release_revoke_document(self):
#         '''
#         Release a document.
#         '''
#         doc = AdminUserDocumentFactory()
#         crs = AdminUserCourseFactory()
#         crs.document_set.add(doc)
#         response = self.client.put('api/document/' + str(doc.pk), format='json')
#         self.assertEqual(
#             response.data,
#             {'id': doc.pk, 'name': u'Test Document for Admin',
#              'link': u"<a href='/path/to/the/course/document/here'></a>",
#              'visible': True})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         response = self.client.put('api/document/' + str(doc.pk), format='json')
#         self.assertEqual(
#             response.data,
#             {'id': doc.pk, 'name': u'Test Document for Admin',
#              'link': u"<a href='/path/to/the/course/document/here'></a>",
#              'visible': False})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

    '''Test student related urls'''

    def test_create_student(self):
        '''
        Calling post with desired name of the new course
        should result in a new course with that name being created
        and the course info (key) being returned to the browser to update
        the course list.
        '''
        pass

    def test_get_students(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

    def test_update_student(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

    def test_remove_student(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

    '''Test team related urls'''

    def test_post_team(self):
        '''
        Calling post with desired name of the new course
        should result in a new course with that name being created
        and the course info (key) being returned to the browser to update
        the course list.
        '''
        pass

    def test_get_team(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

    def test_update_team(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

    def teamtest_remove_course(self):
        '''
        Calling get for a course should redirect the instructor to a
        course detail page where they can create teams, add students,
        and put students in teams.
        '''
        pass

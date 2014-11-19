# import json
#
# from django.test import TestCase, RequestFactory
# from django.test.client import Client
#
# from factories import TeamFactory
#
#
# class TestTeamViews(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.factory = RequestFactory()
#         self.team = TeamFactory()
#         # self.user = UserTeamFactory()
#         self.client.login(username=self.team.user.username,
# password="Test_Team")
#
#     def test_home(self):
#         request = self.client.get("/team/home/" +
#                                   str(self.team.id) + '/')
#  #       self.assertTemplateUsed(request,
#  #                               'main/ccnmtl/home_dash/ccnmtl_home.html')

#     def test_get_course_details(self):
#         '''
#         Requesting the course details page should redirect
#         the admin to a course dashboard where they can create
#         teams and students, and put students in teams.
#         '''
#         self.admin_course = AdminUserCourseFactory()
#         request = self.client.get("/course_details/" +
#                                   str(self.admin_course.pk) + '/')
#         self.assertTemplateUsed(request,
#                                 'main/ccnmtl/course_dash/course_home.html')
# class TestTeamViews(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.factory = RequestFactory()
#         self.team = TeamFactory()
#         self.client.login(username=self.team, password="Test_Team")
#
#     def test_home(self):
#         '''
#         Student logs in as team and sees team home page.
#         '''
#         request = self.client.get("/team/home/" +
#                                   str(self.team.user.pk) + '/')
#         self.assertTemplateUsed(request,
#                                 'main/team/home_dash/team_home.html')
#
#     def setUp(self):
#         self.client = Client()
#         self.factory = RequestFactory()
# #         self.team = TeamProfileFactory().user
# #         self.client.login(username=self.team.username, password="test")
#
#     def test_home_redirect(self):
#         '''Keep getting random bootstrap can't be compressed errors.'''
#         pass
# #         request = self.client.get("/", follow=True)
# #         self.assertEquals(
# #             response.redirect_chain[0],
# #             ('http://testserver/teacher/' +
# #              str(self.teacher.profile.pk) + '/',
# #              302))
# #         self.assertTemplateUsed(response,
# #                                 'main/ccnmtl/ccnmtl_home.html')
#
#     def test_home(self):
#         '''
#         See what happens if I request appropriate home directly
#         instead of following redirect.
#         '''
#         pass
# #         request = self.client.get("/team/" +
# str(self.team.profile.pk) + '/')
# #         self.assertTemplateUsed(request,
# #                                 'main/team/team_home.html')

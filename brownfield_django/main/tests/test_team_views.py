# # import json
# # from datetime import datetime
#
# from django.test import TestCase, RequestFactory
# from django.test.client import Client
# # from django.contrib.auth.models import User
#
# from factories import TeamProfileFactory
# # , \ UserFactory, UserProfileFactory,
# #    StudentProfileFactory, CourseFactory, TeamFactory
#
#
# class TestTeamLogin(TestCase):
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

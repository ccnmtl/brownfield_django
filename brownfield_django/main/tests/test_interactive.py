from django.test import TestCase, RequestFactory
from django.test.client import Client
from factories import ViewsAdminProfileFactory, ViewsTeacherProfileFactory, \
    TeamFactory

from brownfield_django.main.xml_strings import INITIAL_XML


class TestAdminInfoInteractiveViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.admin = ViewsAdminProfileFactory().user
        self.client.login(username=self.admin.username, password="Admin")

    def test_admin_info_get_interaction(self):
        response = self.client.get("/demo/info/")
        self.assertEqual(response.content,
                                "<data><response>OK</response></data>")

    def test_admin_info_post_interaction(self):
        response = self.client.post("/demo/info/")
        self.assertEqual(response.content,
                                "<data><response>OK</response></data>")


class TestInstructorInfoInteractiveViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.inst = ViewsTeacherProfileFactory().user
        self.client.login(username=self.inst.username, password="Teacher")

    def test_instructor_info_get_interaction(self):
        response = self.client.get("/demo/info/")
        self.assertEqual(response.content, INITIAL_XML)

    def test_instructor_info_post_interaction(self):
        response = self.client.post("/demo/info/")
        self.assertEqual(response.content,
                                "<data><response>OK</response></data>")


class TestAdminHistoryInteractiveViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.admin = ViewsAdminProfileFactory().user
        self.client.login(username=self.admin.username, password="Admin")

    def test_admin_history_get_interaction(self):
        response = self.client.get("/demo/history/")
        self.assertEqual(response.content,
                                INITIAL_XML)

    def test_admin_history_post_interaction(self):
        response = self.client.post("/demo/history/")
        self.assertEqual(response.content,
                                INITIAL_XML)


class TestInstructorHistoryInteractiveViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.inst = ViewsTeacherProfileFactory().user
        self.client.login(username=self.inst.username, password="Teacher")

    def test_instructor_history_get_interaction(self):
        response = self.client.get("/demo/history/")
        self.assertEqual(response.content,
                                INITIAL_XML)

    def test_instructor_history_post_interaction(self):
        response = self.client.post("/demo/history/")
        self.assertEqual(response.content,
                                INITIAL_XML)


class TestAdminTestInteractiveViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.admin = ViewsAdminProfileFactory().user
        self.client.login(username=self.admin.username, password="Admin")

    def test_admin_test_get_interaction(self):
        response = self.client.get("/demo/test/")
        self.assertEqual(response.content,
                                INITIAL_XML)

    def test_admin_test_post_interaction(self):
        response = self.client.post("/demo/test/")
        self.assertEqual(response.content,
                                INITIAL_XML)


class TestInstructorTestInteractiveViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.inst = ViewsTeacherProfileFactory().user
        self.client.login(username=self.inst.username, password="Teacher")

    def test_test_history_get_interaction(self):
        response = self.client.get("/demo/test/")
        self.assertEqual(response.content,
                                INITIAL_XML)

    def test_test_history_post_interaction(self):
        response = self.client.post("/demo/test/")
        self.assertEqual(response.content,
                                INITIAL_XML)


# '''Tests for Team Views of Interactive'''
# 
# 
# class TestTeamInfoInteractiveViews(TestCase):
# 
#     def setUp(self):
#         self.client = Client()
#         self.factory = RequestFactory()
#         self.team = TeamFactory()
#         self.team_user = self.team.user
#         self.client.login(username=self.team_user.username, password="Test_Team")
# 
#     def test_team_recon_info(self):
# #         team_pk = self.team.pk
# #         self.assertEqual(self.team.pk, self.team_user.pk)
#         response = self.client.post("/team/1/info/",
#         #" + str(self.team.pk) + "/info/",
#                                     {'infoType': 'recon',
#                                      'date': '2014/9/19 13:26',
#                                      'description': 'Performed visual reconnaissance.',
#                                      'cost': '100', 'internalName': 'internalName'})
#         self.assertEqual(response.content,
#                                 "<data><response>OK</response></data>")

# class TeamInfoView(CSRFExemptMixin, View):
# 
#     def post(self, request, pk):
#         team = Team.objects.get(user=request.user)
#         infoType = request.POST['infoType']
# 
#         if infoType == "recon":
#             th = History.objects.create(
#                 team=team,
#                 date=request.POST['date'],
#                 description=request.POST['description'],
#                 cost=request.POST['cost'])
#             inf = Information.objects.create(
#                 history=th,
#                 infoType=request.POST['infoType'],
#                 internalName=request.POST['internalName'])
#             return HttpResponse("<data><response>OK</response></data>")
# 
#         elif infoType == "visit":
#             th = History.objects.create(
#                 team=team,
#                 date=request.POST['date'],
#                 description=request.POST['description'],
#                 cost=request.POST['cost'])
#             th.save()
#             inf = Information.objects.create(
#                 history=th,
#                 internalName=request.POST['internalName'],
#                 infoType=request.POST['infoType'])
#             return HttpResponse("<data><response>OK</response></data>")
# 
#         elif infoType == "question":
#             th = History.objects.create(
#                 team=team,
#                 date=request.POST['date'],
#                 description=request.POST['description'],
#                 cost=request.POST['cost'])
#             inf = Information.objects.create(
#                 history=th,
#                 internalName=request.POST['internalName'],
#                 infoType=request.POST['infoType'])
#             return HttpResponse("<data><response>OK</response></data>")
# 
#         elif infoType == "doc":
#             th = History.objects.create(
#                 team=team,
#                 date=request.POST['date'],
#                 description=request.POST['description'],
#                 cost=request.POST['cost'])
#             inf = Information.objects.create(
#                 history=th,
#                 internalName=request.POST['internalName'],
#                 infoType=request.POST['infoType'])
#             inf.save()
#             return HttpResponse("<data><response>OK</response></data>")
# 
#
# 
#     def test_admin_info_post_interaction(self):
#         response = self.client.post("/demo/info/")
#         self.assertEqual(response.content,
#                                 "<data><response>OK</response></data>")

# 
# (r'^team/home/(?P<pk>\d+)/$', TeamHomeView.as_view()),
#     (r'^team/(?P<pk>\d+)/play$', TeamHistoryView.as_view()),
#     (r'^team/(?P<pk>\d+)/history/', TeamHistoryView.as_view()),
#     (r'^team/(?P<pk>\d+)/info/$', TeamInfoView.as_view()),
#     (r'^team/(?P<pk>\d+)/test/$', TeamPerformTest.as_view()),
# class TeamHistoryView(CSRFExemptMixin, View):
#     """Need to parse the XML and substitute the correct
#     values for each student interaction."""
# 
#     def send_team_history(self, team):
#         template = loader.get_template(
#             'main/team/bfaxml.txt')
#         history = History.objects.filter(team=team)
#         team_info = Information.objects.filter(history=history)
#         tests_perf = PerformedTest.objects.filter(history=history)
# 
#         ctx = Context({'team': team, 'team_info': team_info,
#                        'team_tests': tests_perf, 'team_history': history})
#         xml_history = template.render(ctx)
#         return xml_history
# 
#     def get(self, request, pk):
#         """Get retrieves the current team values for the flash."""
#         team = Team.objects.get(user=request.user)
#         chk_history = History.objects.filter(team=team)
# 
#         if chk_history.count() == 0:
#             return HttpResponse(TEAM_HISTORY)
#         elif chk_history.count() > 0:
#             # team_info = self.send_team_history(team)
#             return HttpResponse(self.send_team_history(team))
# 
# 
 
# class TeamPerformTest(CSRFExemptMixin, View):
# 
#     def post(self, request, pk):
#         team = Team.objects.get(user=request.user)
# 
#         th = History.objects.create(
#             team=team,
#             date=request.POST['date'],
#             description=request.POST['description'],
#             cost=request.POST['cost'])
#         pf = PerformedTest.objects.create(
#             history=th,
#             x=int(request.POST['x']),
#             y=int(request.POST['y']),
#             testNumber=int(request.POST['testNumber']))
#         try:
#             pf.z = request.POST['z']
#             pf.save()
#         except:
#             pass
#         try:
#             pf.testDetails = request.POST['testDetails']
#             pf.save()
#         except:
#             pass
#         try:
#             pf.paramString = request.POST['paramString']
#             pf.save()
#         except:
#             pass
#         return HttpResponse("<data><response>OK</response></data>")

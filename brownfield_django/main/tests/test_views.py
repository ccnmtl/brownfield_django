from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.test.client import Client

from brownfield_django.main.tests.factories import (
    HistoryFactory, InformationFactory, PerformedTestFactory,
    UserFactory, UserProfileFactory, TeamFactory, CourseFactory
)
from brownfield_django.main.views import TeamHistoryView


class BasicTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 302)
        # we want it to redirect to login,
        # that is current behavior of site

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)
        assert "PASS" in response.content


class HomeViewTest(TestCase):
    def test_get_as_anon_user(self):
        r = self.client.get('/', follow=True)
        self.assertEquals(r.status_code, 200)

    def test_get_as_student(self):
        u = UserFactory()
        UserProfileFactory(user=u, profile_type='ST')
        team = TeamFactory(user=u)
        team.course = CourseFactory()
        team.save()
        u.set_password('test')
        u.save()
        self.client.login(username=u.username, password='test')

        r = self.client.get('/', follow=True)
        self.assertEquals(r.status_code, 200)

    def test_get_as_teacher(self):
        u = UserFactory()
        UserProfileFactory(user=u, profile_type='TE')
        u.set_password('test')
        u.save()
        self.client.login(username=u.username, password='test')

        r = self.client.get('/', follow=True)
        self.assertEquals(r.status_code, 200)

    def test_get_as_administrator(self):
        u = UserFactory()
        UserProfileFactory(user=u, profile_type='AD')
        u.set_password('test')
        u.save()
        self.client.login(username=u.username, password='test')

        r = self.client.get('/', follow=True)
        self.assertEquals(r.status_code, 200)


class TestAnonymousUserLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_home(self):
        response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.redirect_chain[0],
                          ('/accounts/login/?next=/', 302))


class TestAnonymousTeamHome(TestCase):
    def setUp(self):
        self.client = Client()

    def test_denied(self):
        t = TeamFactory()
        r = self.client.get("/team/home/%d/" % t.pk)
        self.assertEqual(r.status_code, 403)


class TestCSV(TestCase):

    def test_get(self):
        team = TeamFactory()

        InformationFactory(history=HistoryFactory(team=team))
        InformationFactory(history=HistoryFactory(team=team))

        PerformedTestFactory(history=HistoryFactory(team=team), testNumber=5)
        PerformedTestFactory(history=HistoryFactory(team=team))

        self.client.login(username=team.user.username, password='test')

        url = reverse('team-csv', kwargs={'pk': team.user.pk})
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)

        a = response.content.splitlines()
        self.assertEquals(a[0], 'Cost,Date,Description,X,Y,Z')
        self.assertEquals(a[1], '100,2014/10/23 13:14,History Record')
        self.assertEquals(a[2], '100,2014/10/23 13:14,History Record')
        self.assertEquals(a[3], '100,2014/10/23 13:14,History Record,10,30,60')
        self.assertEquals(a[4],
                          '100,2014/10/23 13:14,History Record,10,30,None')


class TestTeamHistoryView(TestCase):

    def setUp(self):
        self.view = TeamHistoryView()
        self.team = TeamFactory()

        InformationFactory(history=HistoryFactory(team=self.team))
        PerformedTestFactory(history=HistoryFactory(team=self.team))

    def test_initial_team_history(self):
        result = ('<bfaxml> <config> <user signedcontract="False"'
                  ' startingbudget="" realname="{}"> </user> '
                  '<narrative enabled=""></narrative> <information> '
                  '</information> </config> <testdata> </testdata> <budget> '
                  '</budget> </bfaxml>').format(self.team.user.username)

        xml = self.view.initial_team_history(self.team)
        xml = ' '.join(xml.split())
        self.assertEquals(xml, result)

    def test_send_team_history(self):
        result = (
            '<bfaxml> <config> <user realname="{}" '
            'signedcontract="False" startingbudget="" /> '
            '<narrative enabled="" /> <information> <info type="recon" '
            'name="recon"></info> </information> </config> <testdata> '
            '<test y="30" x="10" n="1" testNumber="1" paramString="'
            'Still need to find format for these..." z="60" ></test> '
            '</testdata> <budget> <i a="100" t="2014/10/23 13:14" '
            'd="History Record"></i> <i a="100" t="2014/10/23 13:14" '
            'd="History Record"></i> </budget> </bfaxml>'
        ).format(self.team.user.username)

        xml = self.view.send_team_history(self.team)
        xml = ' '.join(xml.split())
        self.assertEquals(xml, result)

    def test_get(self):
        url = reverse('team-history', kwargs={'pk': self.team.id})
        self.client.login(username=self.team.user.username, password='test')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class RestrictedFlatPageTest(TestCase):

    def setUp(self):
        site = Site.objects.get(id=1)
        site.name = 'sport'
        site.save()

        self.page = FlatPage.objects.create(
            registration_required=True,
            url='/instructors/test/', title='Foo', content="Hello World")
        self.page.sites.add(site)

    def test_anonymous(self):
        response = self.client.get('/instructors/test/')
        self.assertEquals(response.status_code, 302)

    def test_student(self):
        u = UserFactory()
        UserProfileFactory(user=u, profile_type='ST')
        self.client.login(username=u.username, password='test')

        response = self.client.get('/instructors/test/')
        self.assertEquals(response.status_code, 302)

    def test_teacher(self):
        u = UserFactory()
        UserProfileFactory(user=u, profile_type='TE')

        self.client.login(username=u.username, password='test')

        response = self.client.get('/instructors/test/')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Hello World' in response.content)

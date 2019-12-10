import os

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import django.views.static
import flashpolicies.views
from rest_framework import routers

from brownfield_django.main.views import CourseViewSet, UserViewSet, \
    DocumentViewSet, StudentViewSet, TeamViewSet, InstructorViewSet, \
    RestrictedFlatPage, RestrictedFile
from brownfield_django.main.views import (
    HomeView, CCNMTLHomeView, CCNMTLCourseDetail,
    TeamHomeView, EditTeamsView, ShowTeamsView,
    ActivateCourseView, BrownfieldDemoView,
    TeamHistoryView, TeamInfoView, TeamPerformTest,
    TeamCSV, ShowProfessorsView, ArchiveCourseView, TeamSignContract)


admin.autodiscover()

simulation_root = os.path.join(os.path.dirname(__file__),
                               '../media/', 'flash')

auth_urls = url(r'^accounts/', include('django.contrib.auth.urls'))

if hasattr(settings, 'CAS_BASE'):
    auth_urls = url(r'^accounts/', include('djangowind.urls'))


router = routers.DefaultRouter()
router.register(r'course', CourseViewSet)
router.register(r'user', UserViewSet)
router.register(r'document', DocumentViewSet)
router.register(r'student', StudentViewSet)
router.register(r'instructor', InstructorViewSet)
# flash uses team in url, this is router for team on dashboard
router.register(r'eteam', TeamViewSet)

try:
    static_flash_domain = settings.AWS_STORAGE_BUCKET_NAME + \
        '.s3.amazonaws.com'
except AttributeError:
    static_flash_domain = settings.STATIC_URL

urlpatterns = [
    auth_urls,
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^$', HomeView.as_view()),
    url(r'^ccnmtl/home/(?P<pk>\d+)/$', CCNMTLHomeView.as_view()),
    url(r'^course_details/(?P<pk>\d+)/$', CCNMTLCourseDetail.as_view()),
    url(r'^activate_course/(?P<pk>\d+)/$', ActivateCourseView.as_view()),
    url(r'^archive_course/(?P<pk>\d+)/$', ArchiveCourseView.as_view()),
    url(r'^edit_teams/(?P<pk>\d+)/$', EditTeamsView.as_view()),
    url(r'^show_teams/(?P<pk>\d+)/$', ShowTeamsView.as_view()),
    url(r'^show_instructors/$', ShowProfessorsView.as_view()),
    url(r'^demo/play$', TemplateView.as_view(
        template_name="main/flvplayer.html")),
    url(r'^demo/info/', BrownfieldDemoView.as_view()),
    url(r'^demo/history/', BrownfieldDemoView.as_view()),
    url(r'^demo/test/$', BrownfieldDemoView.as_view()),
    url(r'^team/home/(?P<pk>\d+)/$',
        TeamHomeView.as_view(), name="team-home"),
    url(r'^team/(?P<pk>\d+)/play$', TeamHistoryView.as_view(),
        name='team-history'),
    url(r'^team/(?P<pk>\d+)/history/', TeamHistoryView.as_view()),
    url(r'^team/(?P<pk>\d+)/info/$', TeamInfoView.as_view()),
    url(r'^team/(?P<pk>\d+)/test/$', TeamPerformTest.as_view()),
    url(r'^team/sign_contract/$',
        TeamSignContract.as_view(), name='sign-contract'),
    url(r'^site_history/$', TemplateView.as_view(
        template_name="interactive/site_history.html")),
    url(r'^team_csv/(?P<pk>\d+)/$', TeamCSV.as_view(), name='team-csv'),
    url(r'^crossdomain.xml$', flashpolicies.views.simple, {
        'domains': [static_flash_domain, '*.ccnmtl.columbia.edu']
    }),
    url('^contact/', include('contactus.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^_impersonate/', include('impersonate.urls')),
    url(r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'^instructors/files/(?P<path>.*)$', RestrictedFile.as_view()),
    url(r'^instructors/', RestrictedFlatPage.as_view()),

    url(r'^simulation/demo/$', TemplateView.as_view(
        template_name='simulation/demo.html')),

    url(r'^simulation/walkthrough/(?P<path>.*)$',
        django.views.static.serve,
        {'document_root': simulation_root}),

    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT})
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]

import os

from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.views.generic import TemplateView
import django.views.static
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

auth_urls = path('accounts/', include('django.contrib.auth.urls'))

if hasattr(settings, 'CAS_BASE'):
    auth_urls = path('accounts/', include('djangowind.urls'))


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
    path('accounts/', include('registration.backends.default.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    path('', HomeView.as_view()),
    re_path(r'^ccnmtl/home/(?P<pk>\d+)/$', CCNMTLHomeView.as_view()),
    re_path(r'^course_details/(?P<pk>\d+)/$', CCNMTLCourseDetail.as_view()),
    re_path(r'^activate_course/(?P<pk>\d+)/$', ActivateCourseView.as_view()),
    re_path(r'^archive_course/(?P<pk>\d+)/$', ArchiveCourseView.as_view()),
    re_path(r'^edit_teams/(?P<pk>\d+)/$', EditTeamsView.as_view()),
    re_path(r'^show_teams/(?P<pk>\d+)/$', ShowTeamsView.as_view()),
    path('show_instructors/', ShowProfessorsView.as_view()),
    path('demo/play', TemplateView.as_view(
        template_name="main/flvplayer.html")),
    path('demo/info/', BrownfieldDemoView.as_view()),
    path('demo/history/', BrownfieldDemoView.as_view()),
    path('demo/test/', BrownfieldDemoView.as_view()),
    re_path(r'^team/home/(?P<pk>\d+)/$',
        TeamHomeView.as_view(), name="team-home"),
    re_path(r'^team/(?P<pk>\d+)/play$', TeamHistoryView.as_view(),
        name='team-history'),
    re_path(r'^team/(?P<pk>\d+)/history/', TeamHistoryView.as_view()),
    re_path(r'^team/(?P<pk>\d+)/info/$', TeamInfoView.as_view()),
    re_path(r'^team/(?P<pk>\d+)/test/$', TeamPerformTest.as_view()),
    re_path('team/sign_contract/',
        TeamSignContract.as_view(), name='sign-contract'),
    path('site_history/', TemplateView.as_view(
        template_name="interactive/site_history.html")),
    re_path(r'^team_csv/(?P<pk>\d+)/$', TeamCSV.as_view(), name='team-csv'),
    path('contact/', include('contactus.urls')),
    path('admin/', admin.site.urls),
    path('_impersonate/', include('impersonate.urls')),
    path('stats/', TemplateView.as_view(template_name="stats.html")),
    path('smoketest/', include('smoketest.urls')),
    re_path(r'^instructors/files/(?P<path>.*)$', RestrictedFile.as_view()),
    path('instructors/', RestrictedFlatPage.as_view()),

    path('simulation/demo/', TemplateView.as_view(
        template_name='simulation/demo.html')),

    re_path(r'^simulation/walkthrough/(?P<path>.*)$',
        django.views.static.serve,
        {'document_root': simulation_root}),

    re_path(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT})
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

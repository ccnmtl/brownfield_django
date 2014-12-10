from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
# from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rest_framework import routers

from brownfield_django.main.views import CourseViewSet, UserViewSet, \
    DocumentViewSet, StudentViewSet
from brownfield_django.main.views import HomeView, AdminTeamView, \
    CCNMTLHomeView, CCNMTLCourseDetail, \
    TeamHomeView, EditTeamsView, ShowTeamsView, ActivateCourseView, \
    BrownfieldInfoView, BrownfieldHistoryView, BrownfieldTestView, \
    TeamHistoryView, TeamInfoView, TeamPerformTest, InstructorViewSet, \
    TeamCSV, ShowProfessorsView


admin.autodiscover()

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)

auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))

logout_page = (r'^accounts/logout/$',
               'django.contrib.auth.views.logout',
               {'next_page': redirect_after_logout})
admin_logout_page = (r'^accounts/logout/$',
                     'django.contrib.auth.views.logout',
                     {'next_page': '/admin/'})

if hasattr(settings, 'CAS_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (r'^accounts/logout/$',
                   'djangowind.views.logout',
                   {'next_page': redirect_after_logout})
    admin_logout_page = (r'^admin/logout/$',
                         'djangowind.views.logout',
                         {'next_page': redirect_after_logout})


router = routers.DefaultRouter()
router.register(r'course', CourseViewSet)
router.register(r'user', UserViewSet)
router.register(r'document', DocumentViewSet)
router.register(r'student', StudentViewSet)
router.register(r'instructor', InstructorViewSet)

urlpatterns = patterns(
    '',
    logout_page,
    admin_logout_page,
    auth_urls,
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    (r'^$', HomeView.as_view()),
    (r'^ccnmtl/home/(?P<pk>\d+)/$', CCNMTLHomeView.as_view()),
    (r'^admin_team/$', AdminTeamView.as_view()),
    (r'^admin_team/(?P<pk>\d+)/$', AdminTeamView.as_view()),
    (r'^course_details/(?P<pk>\d+)/$', CCNMTLCourseDetail.as_view()),
    (r'^activate_course/(?P<pk>\d+)/$', ActivateCourseView.as_view()),
    (r'^edit_teams/(?P<pk>\d+)/$', EditTeamsView.as_view()),
    (r'^show_teams/(?P<pk>\d+)/$', ShowTeamsView.as_view()),
    (r'^show_instructors/$', ShowProfessorsView.as_view()),
    (r'^demo/play$', TemplateView.as_view(
        template_name="main/flvplayer.html")),
    (r'^demo/info/', BrownfieldInfoView.as_view()),
    (r'^demo/history/', BrownfieldHistoryView.as_view()),
    (r'^demo/test/$', BrownfieldTestView.as_view()),
    (r'^team/home/(?P<pk>\d+)/$', TeamHomeView.as_view()),
    (r'^team/(?P<pk>\d+)/play$', TeamHistoryView.as_view()),
    (r'^team/(?P<pk>\d+)/history/', TeamHistoryView.as_view()),
    (r'^team/(?P<pk>\d+)/info/$', TeamInfoView.as_view()),
    (r'^team/(?P<pk>\d+)/test/$', TeamPerformTest.as_view()),
    (r'^site_history/$', TemplateView.as_view(
        template_name="interactive/site_history.html")),
    (r'^team_csv/(?P<username>.*)/$', TeamCSV.as_view()),
    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

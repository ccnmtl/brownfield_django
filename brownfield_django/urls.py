from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
import django.contrib.auth.views
from django.views.generic import TemplateView
import django.views.static
import djangowind.views
import flashpolicies.views
from rest_framework import routers

from brownfield_django.main.views import CourseViewSet, UserViewSet, \
    DocumentViewSet, StudentViewSet, TeamViewSet, InstructorViewSet
from brownfield_django.main.views import HomeView, \
    CCNMTLHomeView, CCNMTLCourseDetail, \
    TeamHomeView, EditTeamsView, ShowTeamsView, ActivateCourseView, \
    BrownfieldInfoView, BrownfieldHistoryView, BrownfieldTestView, \
    TeamHistoryView, TeamInfoView, TeamPerformTest, \
    TeamCSV, ShowProfessorsView, ArchiveCourseView, TeamSignContract


admin.autodiscover()

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)

auth_urls = url(r'^accounts/', include('django.contrib.auth.urls'))

logout_page = url(r'^accounts/logout/$', django.contrib.auth.views.logout,
                  {'next_page': redirect_after_logout})
admin_logout_page = url(r'^accounts/logout/$',
                        django.contrib.auth.views.logout,
                        {'next_page': '/admin/'})

if hasattr(settings, 'CAS_BASE'):
    auth_urls = url(r'^accounts/', include('djangowind.urls'))
    logout_page = url(r'^accounts/logout/$',
                      djangowind.views.logout,
                      {'next_page': redirect_after_logout})
    admin_logout_page = url(r'^admin/logout/$',
                            djangowind.views.logout,
                            {'next_page': redirect_after_logout})


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
    logout_page,
    admin_logout_page,
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
    url(r'^demo/info/', BrownfieldInfoView.as_view()),
    url(r'^demo/history/', BrownfieldHistoryView.as_view()),
    url(r'^demo/test/$', BrownfieldTestView.as_view()),
    url(r'^team/home/(?P<pk>\d+)/$', TeamHomeView.as_view()),
    url(r'^team/(?P<pk>\d+)/play$', TeamHistoryView.as_view(),
        name='team-history'),
    url(r'^team/(?P<pk>\d+)/history/', TeamHistoryView.as_view()),
    url(r'^team/(?P<pk>\d+)/info/$', TeamInfoView.as_view()),
    url(r'^team/(?P<pk>\d+)/test/$', TeamPerformTest.as_view()),
    url(r'^team/sign_contract/$', TeamSignContract.as_view()),
    url(r'^site_history/$', TemplateView.as_view(
        template_name="interactive/site_history.html")),
    url(r'^team_csv/(?P<username>.*)/$', TeamCSV.as_view(), name='team-csv'),
    url(r'^crossdomain.xml$', flashpolicies.views.simple, {
        'domains': [static_flash_domain, '*.ccnmtl.columbia.edu']
    }),
    url(r'^static/flash/documents/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    url(r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
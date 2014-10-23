import os.path

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
# from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rest_framework import routers

from brownfield_django.main.views import CourseViewSet, UserViewSet, \
    DocumentViewSet, StudentViewSet
from brownfield_django.main.views import DetailJSONCourseView, \
    HomeView, AdminTeamView, CCNMTLHomeView, CCNMTLCourseDetail, \
    TeamHomeView, EditTeamsView, ShowTeamsView, ActivateCourseView, \
    BrownfieldInfoView, BrownfieldHistoryView, BrownfieldTestView


admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

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
    (r'^team/home/(?P<pk>\d+)/$', TeamHomeView.as_view()),
    (r'^team/$', AdminTeamView.as_view()),
    (r'^team/(?P<pk>\d+)/$', AdminTeamView.as_view()),
    (r'^course_details/(?P<pk>\d+)/$', CCNMTLCourseDetail.as_view()),
    (r'^activate_course/(?P<pk>\d+)$', ActivateCourseView.as_view()),
    (r'^edit_teams/(?P<pk>\d+)/$', EditTeamsView.as_view()),
    (r'^show_teams/(?P<pk>\d+)/$', ShowTeamsView.as_view()),
    (r'^update_course/(?P<pk>\d+)$', DetailJSONCourseView.as_view()),
    # Demo View
    (r'^demo/play$', TemplateView.as_view(
        template_name="main/flvplayer.html")),
    (r'^demo/info/$', BrownfieldInfoView.as_view()),
    # "brownfield_django.main.views.get_demo_info"),
    (r'^demo/history/', BrownfieldHistoryView.as_view()),
    (r'^demo/test/$', BrownfieldTestView.as_view()),
    (r'^demo/save/$', "brownfield_django.main.views.demo_save"),
    (r'^site_history/$', TemplateView.as_view(
        template_name="interactive/site_history.html")),
    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

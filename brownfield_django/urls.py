from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import TemplateView
from pagetree.generic.views import PageView, EditView, InstructorView
from brownfield_django.main.views import StudentHomeView, \
    HomeView, RegistrationView, DemoHomeView, \
    TeacherHomeView, TeacherCourseDetail, TeacherCreateCourse, \
    TeacherAddStudent, TeacherCreateTeam, TeacherEditTeam, \
    TeacherDeleteTeam, TeacherReleaseDocument, TeacherRevokeDocument, \
    TeacherBBHomeView
    
from brownfield_django.main.forms import CreateAccountForm
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (
    r'^accounts/logout/$',
    'django.contrib.auth.views.logout',
    {'next_page': redirect_after_logout})
if hasattr(settings, 'WIND_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (
        r'^accounts/logout/$',
        'djangowind.views.logout',
        {'next_page': redirect_after_logout})


urlpatterns = patterns(
    '',
    auth_urls,
    logout_page,
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/register/$', RegistrationView.as_view(
        form_class=CreateAccountForm),
        name='register'),
    (r'^demo/$', TemplateView.as_view(template_name="main/demo.html")),
    #/media/history/?cachebuster=0.664656763430685

    #url(r'^home_demo/$', DemoHomeView.as_view(), name="home"),
    #url(r'^$', HomeView.as_view(), name="home"),
    #(r'^demo/play/(?P<map_id>\d+)/display/flashConduit$', TemplateView.as_view(template_name="main/flvplayer.html")),
    (r'^demo/play$', "brownfield_django.main.views.get_demo"),#TemplateView.as_view(template_name="main/flvplayer.html")),
    (r'^demo/media/flash/$', "brownfield_django.main.views.get_bfa"),
    (r'^demo/history/$', "brownfield_django.main.views.get_demo_history"),
    url(r'^media/history/?cachebuster=(\d+.?d+)$', DemoHomeView.as_view()), # Doesn't seem to work
    url(r'^media/history/?cachebuster=(.*)$', DemoHomeView.as_view()), # Doesn't seem to work
    #([0-9]{15}\.[0-9]{15})
    # ([0-9]+) should it be ?cachebuster=(([0-9]+)(.?)([0-9]+))$ instead?
    # almost? url(r'^media/history/?cachebuster=(?\d+.?\d*)$', DemoHomeView.as_view()),
    #url(r'^media/history/?cachebuster=(/d*.?d*/)$', DemoHomeView.as_view()),
    (r'^demo/info/$', "brownfield_django.main.views.get_demo_info"),
    (r'^demo/test/$', "brownfield_django.main.views.get_demo_test"),
    (r'^demo/save/$', "brownfield_django.main.views.demo_save"),
    (r'^visrecon/$', TemplateView.as_view(template_name="interactive/visrecon.html")),
    (r'^demo/$', TemplateView.as_view(template_name="interactive/demo_layout.html")),
    (r'^site_history/$', TemplateView.as_view(template_name="interactive/site_history.html")),
    (r'^$', HomeView.as_view()),
    (r'^student/(?P<pk>\d+)/$', StudentHomeView.as_view()),
    
    # Teacher Views
    (r'^teacher/(?P<pk>\d+)/$', TeacherHomeView.as_view()),
    (r'^courses$', TeacherBBHomeView.as_view()),
    (r'^course_detail/(?P<pk>\d+)/$', TeacherCourseDetail.as_view()),
    (r'^create_course/$', TeacherCreateCourse.as_view()),
    (r'^add_student/$', TeacherAddStudent.as_view()),
    (r'^release_document/$', TeacherReleaseDocument.as_view()),
    (r'^revoke_document/$', TeacherRevokeDocument.as_view()),
    (r'^create_team/$', TeacherCreateTeam.as_view()),
    (r'^delete_team/$', TeacherDeleteTeam.as_view()),
    (r'^edit_team/$', TeacherEditTeam.as_view()),
    
    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^quizblock/', include('quizblock.urls')),
    (r'^pages/edit/(?P<path>.*)$', login_required(EditView.as_view(
        hierarchy_name="main",
        hierarchy_base="/pages/")),
     {}, 'edit-page'),
    (r'^pages/instructor/(?P<path>.*)$',
        login_required(InstructorView.as_view(
            hierarchy_name="main",
            hierarchy_base="/pages/"))),
    (r'^pages/(?P<path>.*)$', PageView.as_view(
        hierarchy_name="main",
        hierarchy_base="/pages/")),
)

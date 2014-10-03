import os.path

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from pagetree.generic.views import EditView, InstructorView, PageView

from brownfield_django.main.forms import CreateAccountForm
from brownfield_django.main.views import StudentHomeView, \
    HomeView, RegistrationView, AddStudentView, ListCourseStudentsView, \
    TeacherHomeView, CourseView, TeacherCourseDetail, DocumentView, \
    UserCourseView, AllCourseView, ToggleActivationCourseView
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
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    (r'^$', HomeView.as_view()),
    (r'^teacher/(?P<pk>\d+)/$', TeacherHomeView.as_view()),
    # Teacher Views/document
    # Teacher Course
    (r'^course/$', CourseView.as_view()),
    (r'^course/(?P<pk>\d+)$', CourseView.as_view()),
    (r'^course/(?P<pk>\d+)/$', CourseView.as_view()),
    (r'^course_details/(?P<pk>\d+)/$', TeacherCourseDetail.as_view()),
    (r'^document/$', DocumentView.as_view()),
    (r'^document/(?P<pk>\d+)$', DocumentView.as_view()),
    (r'^user_courses/$', UserCourseView.as_view()),
    (r'^all_courses/$', AllCourseView.as_view()),
    (r'^toggle_activation/(?P<pk>\d+)/$', ToggleActivationCourseView.as_view()),
    # Teacher Student
    (r'^add_student/(?P<pk>\d+)$', AddStudentView.as_view()),
    (r'^list_students/(?P<name>.*)/(?P<pk>\d+)$',
        ListCourseStudentsView.as_view()),
    # Teacher Team View
    (r'^team/(?P<pk>\d+)$', CourseView.as_view()),
    # Teacher Documents
    # (r'^documents/(?P<pk>\d+)$', CourseView.as_view()),
    # Demo View
    (r'^demo/$', TemplateView.as_view(template_name="main/demo.html")),
    (r'^demo/play$', TemplateView.as_view(
        template_name="main/flvplayer.html")),
    (r'^media/history/$', "brownfield_django.main.views.get_demo"),
    (r'^demo/media/flash/$', "brownfield_django.main.views.get_bfa"),
    # ([0-9]{15}\.[0-9]{15})
    # ([0-9]+) should it be ?cachebuster=(([0-9]+)(.?)([0-9]+))$ instead?
    # almost? url(r'^media/history/?cachebuster=(?\d+.?\d*)$',
    # DemoHomeView.as_view()),
    # url(r'^media/history/?cachebuster=(/d*.?d*/)$', DemoHomeView.as_view()),
    (r'^demo/info/$', "brownfield_django.main.views.get_demo_info"),
    (r'^demo/test/$', "brownfield_django.main.views.get_demo_test"),
    (r'^demo/save/$', "brownfield_django.main.views.demo_save"),
    (r'^visrecon/$', TemplateView.as_view(
        template_name="interactive/visrecon.html")),
    (r'^demo/$', TemplateView.as_view(
        template_name="interactive/demo_layout.html")),
    (r'^site_history/$', TemplateView.as_view(
        template_name="interactive/site_history.html")),
    (r'^student/(?P<pk>\d+)/$', StudentHomeView.as_view()),
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

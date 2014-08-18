from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import TemplateView
from pagetree.generic.views import PageView, EditView, InstructorView
from brownfield_django.main.views import StudentView, TeacherView, TeacherCourseDetail, HomeView, RegistrationView
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
    (r'^backbone/$', TemplateView.as_view(template_name="main/backbone_courses.html")),
    (r'^visrecon/$', TemplateView.as_view(template_name="interactive/visrecon.html")),
    (r'^demo/$', TemplateView.as_view(template_name="interactive/demo_layout.html")),
    (r'^site_history/$', TemplateView.as_view(template_name="interactive/site_history.html")),
    (r'^testing/$', TemplateView.as_view(template_name="interactive/testing.html")),
    (r'^test2/$', TemplateView.as_view(template_name="interactive/test2.html")),
    (r'^test3/$', TemplateView.as_view(template_name="interactive/test3.html")),
    (r'^$', HomeView.as_view()),
    (r'^student/(?P<pk>\d+)/$', StudentView.as_view()),
    (r'^teacher/(?P<pk>\d+)/$', TeacherView.as_view()),
    (r'^course_detail/(?P<pk>\d+)/$', TeacherCourseDetail.as_view()),
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

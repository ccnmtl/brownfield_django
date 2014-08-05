from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import TemplateView
from pagetree.generic.views import PageView, EditView, InstructorView
from brownfield_django.main import views
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
    (r'^registration/', include('registration.backends.default.urls')),
    (r'^$', views.Home.as_view()),
    (r'^contexts/$', views.new_homepage),
    (r'^get_new_courses/$', views.get_new_courses),
    #(r'^course_detail/(?P<pk>\d+)/$', views.CourseDetailView.as_view()),
    (r'^course_detail/(?P<pk>\d+)/$', views.get_course_documents),
    (r'^create_new_course/$', views.create_new_course),
    (r'^course_list/$', views.CourseView.as_view()),
    (r'^add_course/$', views.CreateCourseView.as_view()),
    (r'^home/$', views.Homepage.as_view()),
    (r'^thank_you/$', views.ThankYou.as_view()),
    (r'^course/(?P<pk>\d+)/$', views.UpdateCourseView.as_view()),
    (r'^update_course/(?P<pk>\d+)/$', views.UpdateCourseView.as_view()),
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

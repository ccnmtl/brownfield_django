from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from brownfield_django.main.models import Course, Team, Student
from pagetree.generic.views import EditView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView

class IndexView(TemplateView):
    template_name = "main/index.html"

class CourseView(TemplateView):
    template_name = "main/course_list.html"

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        student_courses = Student.objects.filter(user=self.request.user.pk)
        context['user_courses'] = Course.objects.filter(student=student_courses)

class CreateCourseView(CreateView):
    '''generic class based view for
    adding a course'''
    model = Course
    #template_name = 'icap/add_school.html'
    #success_url = '/thank_you/'

class UpdateCourseView(UpdateView):
    '''generic class based view for
    editing a school'''
    model = Course
#    template_name = 'icap/add_school.html'
#    success_url = '/thank_you/'



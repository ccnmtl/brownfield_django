import json
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from brownfield_django.main.models import Course, Team, Student
from pagetree.generic.views import EditView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView

class IndexView(TemplateView):
    template_name = "main/index.html"

'''According to docs I am currently looking at Ajax must be done with an object-based form view'''

class AjaxableResponseMixin(object):
    """
    Taken from Django Docs
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response




class CourseView(TemplateView):
    template_name = "main/course_list.html"

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        student_courses = Student.objects.filter(user=self.request.user.pk)
        context['user_courses'] = Course.objects.filter(student=student_courses)

class CreateCourseView(AjaxableResponseMixin, CreateView):
    '''generic class based view for
    adding a course'''
    model = Course
    fields = ["name", "startingBudget", "enableNarrative", "message", "active"]
    template_name = 'main/add_course.html'
    #success_url = '/thank_you/'

class UpdateCourseView(AjaxableResponseMixin, UpdateView):
    '''generic class based view for
    editing a school'''
    model = Course
    fields = ['']
#    template_name = 'icap/add_school.html'
#    success_url = '/thank_you/'




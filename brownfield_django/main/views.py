import json
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin
from brownfield_django.main.models import Course, Team, Student, Document
from pagetree.generic.views import EditView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.forms import ModelForm
from django.shortcuts import render

class IndexView(TemplateView):
    template_name = "main/index.html"

class ThankYou(TemplateView):
    template_name = "main/thank_you.html"

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
        print "form invalid"
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


class CourseDetailView(DetailView):
    model = Course
    template_name = "main/course_detail.html"

#    def get(self, request, *args, **kwargs):
#        self.object = self.get_object(queryset=Course.objects.all())
#        return super(CourseDetailView, self).get(request, *args, **kwargs)

#    def get_context_data(self, **kwargs):
#        context = super(CourseDetailView, self).get_context_data(**kwargs)
#        context['documents'] = self.object.document_set.all()
#        return context

#    def get_queryset(self):
#        return self.object.document_set.all()
#    def get_context_data(self, **kwargs):
#        context = super(CourseDetailView, self).get_context_data(**kwargs)
#        context['documents'] =Course.document_set.all(pk=object)
#        return context


class CreateCourseView(AjaxableResponseMixin, CreateView):
    '''generic class based view for
    adding a course'''
    model = Course
    fields = ["name", "startingBudget", "enableNarrative", "message", "active"]
    template_name = 'main/add_course.html'
    success_url = '/thank_you/'

class UpdateCourseView(AjaxableResponseMixin, UpdateView):
    '''generic class based view for
    editing a school'''
    model = Course
    fields = ["name", "startingBudget", "enableNarrative", "message", "active"]
    template_name = 'course.html'
#    success_url = '/thank_you/'

class Homepage(AjaxableResponseMixin, CreateView):
    '''Probably a horrble idea and completely wrong...'''
    model = Course
    template_name = 'main/fancy_page.html'
    fields = ["name", "startingBudget", "enableNarrative", "message", "active"]
    success_url = '/thank_you/'

    # I assume there are probably some checks I should do
    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            #new_course = {
            #    'pk': self.object.pk,
            #    'name': self.object.name,
            #    'startingBudget': self.object.startingBudget,
            #    'enableNarrative': self.object.enableNarrative,
            #    'message': self.object.message,
            #    'active': self.object.active,
            #}
            course = Course(pk=self.object.pk, name = self.object.name, startingBudget = self.object.startingBudget, enableNarrative = self.object.enableNarrative, message = self.object.message, active = self.object.active)
            course.save()
            return self.render_to_json_response(course)
        else:
            return response

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ["name", "startingBudget", "enableNarrative", "message", "active"]

def new_homepage(request):
    courses = Course.objects.all()
    student_courses = Student.objects.filter(user=request.user.pk)
    user_courses = Course.objects.filter(student=student_courses)
    create_form = CourseForm()

    return render(request, 'main/contexts.html', {'form': create_form, 'user_courses' : user_courses, 'courses' : courses})

def create_new_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            new_course = form.save()
        else:
            return new_course
    else:
        form = CourseForm()

    return render(request, "main/contexts.html", {'form': form})



def get_new_courses(request):
    courses = Course.objects.all()
    student_courses = Student.objects.filter(user=request.user.pk)
    user_courses = Course.objects.filter(student=student_courses)

    return render(request, 'main/contexts.html', {'user_courses' : user_courses, 'courses' : courses})


def get_course_documents(request, pk):
    course = Course.objects.get(pk=pk)
    print type(course)
    print course
    course_documents = course.document_set.all()#Document.objects.filter(course=course)
    return render(request, 'main/course_detail.html', {'course' : course, 'documents' : course_documents})





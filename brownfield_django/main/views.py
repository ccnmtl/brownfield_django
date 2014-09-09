import json
from datetime import datetime
from xml.dom.minidom import parseString

from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.core.urlresolvers import reverse, reverse_lazy

from brownfield_django.main.models import Course, UserProfile, Document, Team
from brownfield_django.main.forms import CourseForm, TeamForm, CreateAccountForm
from brownfield_django.mixins import LoggedInMixin, LoggedInMixinSuperuser, \
    LoggedInMixinStaff, JSONResponseMixin



'''Moved Views From NEPI Over to Start With'''

class HomeView(LoggedInMixin, View):
    '''redoing so that it simply redirects people where they need to be'''

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user.pk)
        except UserProfile.DoesNotExist:
            return HttpResponseRedirect(reverse('register'))

        if user_profile.is_student():
            url = '/student/%s/' % (user_profile.id)
        if user_profile.is_teacher():
            url = '/teacher/%s/' % (user_profile.id)

        return HttpResponseRedirect(url)


class RegistrationView(FormView):
    template_name = 'registration/registration_form.html'
    form_class = CreateAccountForm
    success_url = '/account_created/'

    def form_valid(self, form):
        form.save()
        return super(RegistrationView, self).form_valid(form)



DEMO_XML = """
<bfaxml xmlns:py="http://purl.org/kid/ns#">
    <config>
            <user access="admin"/>

        <user realname="Team Joe Bob" 
              signedcontract="true" 
              startingbudget="60000"
              />
        <narrative enabled="True"/>
        <information>
            <info type="doc" name="policeReport" />
        </information>
    </config>
    <testdata>
        <test x="0" y="0" n="8" />
        <test x="0" y="0" n="9" z="10" />
        <test x="6" y="6" n="8" paramstring="blurdy blurd" />
        <test x="0" y="2" n="8" />
        <test x="1" y="4" n="8" />
    </testdata>
    <budget>
        <i a="1500" t="2004/08/30/23/11" d="excavation at 0,0" />
        <i a="1500" t="2004/08/30/23/12" d="excavation at 0,2" />
        <i a="200" t="2004/08/30/23/14" d="sgsa at 0,0" />
        <i a="200" t="2004/08/30/23/15" d="sgsa at 1,4" />
        <i a="1" t="2004/08/31/23/15" d="Questioned Al Milankovitch" />
    </budget>
</bfaxml>
"""


BROWNFIELD_XML = """
<bfaxml xmlns:py="http://purl.org/kid/ns#">
  <config>
    <user realname="${record.name}" 
      signedcontract="true" 
      startingbudget="${int(record.course.startingBudget)}" 
      py:attrs="{'access':record.access}"
      />
    <narrative enabled="${record.course.enableNarrative}" />
    <information>
      <info py:for="i in record.info" type="${i.infoType}" name="${i.internalName}"/> 
    </information>
  </config>
  <testdata>
    <test py:for="t in record.tests"
      py:attrs="{'paramstring':t.paramString,'z':t.z}" 
      x="${t.x}" 
      y="${t.y}" 
      n="${t.testNumber}" />
  </testdata>
  <budget>
    <i py:for="t in record.history"
       a="${int(t.cost or 0)}" 
       t="${t.date and t.date.strftime('%Y/%m/%d/%H/%M')}" 
       d="${t.description}" />
  </budget>
</bfaxml>
 """





'''I am using this view to play around with getting the
flash to run'''
class BrownfieldDemoView(View):
    '''Initial view/controller usese templates play, bfaxml
    think like in ssnm it has one page and a second call to the flash app
    base template: play
    over template bfaxml
     
    Added xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    to html header - not sure if I need it
    '''
    template_name = 'main/demo.html'
    success_url = '/'

    def get(self, request):
        return render(request, 'main/flvplayer.html',
            content_type="application/xhtml+xml")


def get_demo(request):
    return HttpResponse(DEMO_XML)
    #return render(request, 'main/flvplayer.html', {'demo': DEMO_XML}, content_type="application/xhtml+xml")

def get_bfa(request):
    '''Flash is making calls to demo/media/flash/bfa.swf
    so we will give it'''
    return render(request, 'main/bfa.swf', content_type="application/xhtml+xml") 

def get_demo_history(request):
    return HttpResponse(DEMO_XML)

INFO_TEST = """
        <information>
            <info type="doc" name="policeReport" />
        </information>
"""

def get_demo_info(request):
    return HttpResponse(DEMO_XML)

def get_demo_test(request):
    return HttpResponse("<data><response>OK</response></data>")

def demo_save(request):
    return HttpResponse("<data><response>OK</response></data>")
        

class DemoHomeView(JSONResponseMixin, View):
    '''Again I'm just using this view to get the Flash working,
    no permissions or users'''
    def get(self, request): #, *args, **kwargs):
        print request.GET
        country_id = kwargs.pop('country_id', None)
        country = get_object_or_404(Country, name=country_id)

        schools = []
        for school in School.objects.filter(country=country):
            schools.append({'id': str(school.id), 'name': school.name})

        return self.render_to_json_response({'schools': schools})

# '''Old code looks like it is making a call to'''
#     
#     (template='kid:brownfield.templates.bfaxml',
#             content_type='application/xml',
#             accept_format='application/xml',
#             fragment=True,
#             )
#     #@identity.require(identity.in_any_group('admin','professor'))
#     def history(self, **kw):
#         class R:
#             name="Brownfield Demo Team"
#             info = []
#             tests = []
#             history = []
#             
#             access = 'professor'
#             if 'admin' in identity.current.groups:
#                 access = 'admin'
#             elif 'professor' in identity.current.groups:
#                 access = 'professor'
#             
#             class C:
#                 startingBudget=0
#                 enableNarrative = True
#             course = C()
#         return dict( record=R() )
#     if not NO_SECURITY:
#         history = identity.require(identity.in_any_group('admin','professor'))(history)
#     
#     @expose()
#     #@identity.require(identity.in_any_group('admin','professor'))
#     def test(self, **kw):
#         return "ok"
#     if not NO_SECURITY:
#         test = identity.require(identity.in_any_group('admin','professor'))(test)
#         
#     @expose()
#     #@identity.require(identity.in_any_group('admin','professor'))
#     def info(self, **kw):
#         return "ok"
#     if not NO_SECURITY:
#         info = identity.require(identity.in_any_group('admin','professor'))(info)


class StudentHomeView(DetailView):
    '''In old application, students are shown a welcome message,
    followed by the instructor's email, and may join or leave teams'''
    model = UserProfile
    template_name = 'main/student/student_home.html'
    #success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(StudentHomeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StudentHomeView, self).get_context_data(**kwargs)
        #context['user_courses'] = Course.objects.filter()
        #context['all_courses'] = Course.objects.all()
        #context['documents'] = Document.objects.all()
        return context


class TeamHomeView(DetailView):
    '''If team has signed their contract they are allowed to play,
    if they have not signed their contract they are redirected
    to the sign contract page.
    the old play page url is: /course/%s/team/%s/play
    the old contract url is: /course/%s/team/%s/contract
    
    @expose(template='kid:brownfield.templates.bfaxml',
            content_type='application/xml',
            accept_format='application/xml',
            fragment=True, #so kid doesn't serve a DOCTYPE HTML declaration
            )
    @expose(template='kid:restresource.templates.view')
    @expose(template='json', accept_format='text/javascript')
    @require_owns_resource()    
    '''
    model = Team
    template_name = 'main/team_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(TeacherView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeacherView, self).get_context_data(**kwargs)
        context['user_courses'] = Course.objects.filter()
        context['all_courses'] = Course.objects.all()
        context['course_form'] = CourseForm()
        context['documents'] = Document.objects.all()
        return context


class TeacherHomeView(DetailView):
    model = UserProfile
    template_name = 'main/instructor/instructor_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(TeacherHomeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeacherHomeView, self).get_context_data(**kwargs)
        context['user_courses'] = Course.objects.filter()
        context['all_courses'] = Course.objects.all()
        context['course_form'] = CourseForm()
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        course_form = CourseForm(self.request.POST)

        if course_form.is_valid():
            course_form.save()
            messages.add_message(self.request, messages.INFO,
                                 'Your changes have been saved.')

            return HttpResponseRedirect('/dashboard/#course-list')

        context = self.get_context_data(object=self.object)
        context['course_form'] = course_form
        return self.render_to_response(context)


class TeacherCourseDetail(DetailView, UpdateView):

    model = Course
    template_name = 'main/instructor/course_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(TeacherCourseDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeacherCourseDetail, self).get_context_data(**kwargs)
        # course documents
        # message
        # course form
        # close course
        # special actions
        context['team_form'] = TeamForm()
        return context
#     def post(self, *args, **kwargs):
#         self.object = self.get_object()
#
#         profile_form = UpdateProfileForm(self.request.POST)
#
#         if profile_form.is_valid():
#             profile_form.save()
#             url = '/%s-dashboard/%s/#user-profile' % (
#                 self.request.user.profile.role(), self.request.user.profile.id)
#             return HttpResponseRedirect(url)
#
#         context = self.get_context_data(object=self.object)
#         context['profile_form'] = profile_form
#         return self.render_to_response(context)


class TeacherCreateCourse(LoggedInMixin, JSONResponseMixin, View):
    '''Do you use forms with ajax views or no?'''
    def send_email(self):
        pass
        
        
    def post(self, *args, **kwargs):
        course = Course()
#        return self.render_to_json_response({'success': True})
        course.name = self.request.POST.get('name')
        course.password = self.request.POST.get('password')
        course.startingBudget = self.request.POST.get('startingBudget')
        course.enableNarrative = self.request.POST.get('enableNarrative')
        course.message = self.request.POST.get('message')
        '''Need to add notification that if they have not added the
        students the students will not recieve the message'''
        course.active = self.request.POST.get('active')
        course.creator = self.request.user.user_profile
        course.save()
        # return HttpResponseRedirect('/dashboard/#user-groups')


class TeacherDeleteCourse(LoggedInMixin, JSONResponseMixin, View):
    '''s'''
    def send_email(self):
        pass
        
        
    def post(self, *args, **kwargs):
        course = Course()
#        return self.render_to_json_response({'success': True})
        course.name = self.request.POST.get('name')
        course.password = self.request.POST.get('password')
        course.startingBudget = self.request.POST.get('startingBudget')
        course.enableNarrative = self.request.POST.get('enableNarrative')
        course.message = self.request.POST.get('message')
        '''Need to add notification that if they have not added the
        students the students will not recieve the message'''
        course.active = self.request.POST.get('active')
        course.creator = self.request.user.user_profile
        course.save()
        # return HttpResponseRedirect('/dashboard/#user-groups')


class TeacherAddStudent(LoggedInMixin, JSONResponseMixin, View):
    '''Add students by adding email, when added send email asking them to go
    to site and create account'''

    def send_email(self):
        pass

    def post(self, *args, **kwargs):
        '''Is uni username? or they create their own?'''
        user = User()
        user.first_name = self.request.POST.get('first_name')
        user.last_name = self.request.POST.get('last_name')
        user.email = self.request.POST.get('password')
        user.save()


class TeacherReleaseDocument(LoggedInMixin, JSONResponseMixin, View):
    '''Will dynamically enable or revoke documents
    - annoying to have page refresh'''

    def send_email(self):
        '''Is an email sent to users/teams that a document has been added?'''
        pass

    def post(self, *args, **kwargs):
        course = get_object_or_404(Document, pk=self.request.POST.get('course'))
        document = get_object_or_404(Document, pk=self.request.POST.get('document'))
        if (self.request.user.profile.is_student() or
            (self.request.user.profile.is_teacher() and
             not course.creator == self.request.user)):
            return HttpResponseForbidden(
                'You are not authorized to release or revoke documents')
        document.visible = True
        document.save()
        return self.render_to_json_response({'success': True})


class TeacherRevokeDocument(LoggedInMixin, JSONResponseMixin, View):
    '''Will dynamically enable or revoke documents
    - annoying to have page refresh'''

    def send_email(self):
        '''Is an email sent to users/teams that a document has been added?'''
        pass

    def post(self, *args, **kwargs):
        course = get_object_or_404(Document, pk=self.request.POST.get('course'))
        document = get_object_or_404(Document, pk=self.request.POST.get('document'))
        if (self.request.user.profile.is_student() or
            (self.request.user.profile.is_teacher() and
             not course.creator == self.request.user)):
            return HttpResponseForbidden(
                'You are not authorized to release or revoke documents')
        document.visible = True
        document.save()
        return self.render_to_json_response({'success': True})


class TeacherCreateTeam(LoggedInMixin, JSONResponseMixin, View):
    pass


class TeacherEditTeam(LoggedInMixin, JSONResponseMixin, View):
    pass


class TeacherDeleteTeam(LoggedInMixin, JSONResponseMixin, View):
    pass






class TeamPerformTest(LoggedInMixin, JSONResponseMixin, View):
    pass

class OnLoad(LoggedInMixin, JSONResponseMixin, View):
    pass
    

class OnSave(LoggedInMixin, JSONResponseMixin, View):
    pass

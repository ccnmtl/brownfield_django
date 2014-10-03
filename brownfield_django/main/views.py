# import json
# from datetime import datetime
# from xml.dom.minidom import parseString
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import XMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from brownfield_django.main.forms import CreateAccountForm  # TeamForm,
from brownfield_django.main.models import Course, UserProfile, Document, Team
from brownfield_django.main.serializers import AddCourseByNameSerializer, \
    CompleteDocumentSerializer, TeamSerializer, CompleteCourseSerializer, \
    CourseNameIDSerializer
from brownfield_django.main.xml_strings import DEMO_XML, INITIAL_XML
from brownfield_django.mixins import LoggedInMixin, JSONResponseMixin, \
    XMLResponseMixin
from brownfield_django.main.document_links import NAME_ONE, \
    LINK_ONE, NAME_TWO, LINK_TWO


class HomeView(LoggedInMixin, View):
    '''redoing so that it simply redirects people where they need to be'''

    def get(self, request):
        print "GET home view"
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
    '''Should I remove the RegistrationView? Professors create Teams
    and add students to the Course...'''

    template_name = 'registration/registration_form.html'
    form_class = CreateAccountForm
    success_url = '/account_created/'

    def form_valid(self, form):
        form.save()
        return super(RegistrationView, self).form_valid(form)


class CourseView(APIView):
    """
    This view interacts with backbone to allow instructors to
    view, add, and edit courses.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None, *args, **kwargs):
        return HttpResponseRedirect("../../course_details/" + str(pk) + "/")

    def post(self, request, format=None, *args, **kwargs):
        '''
        Creating new course with the name requested by user
        with the user as the default professor - will change this later.
        '''
        serializer = AddCourseByNameSerializer(data=request.DATA)
        if serializer.is_valid():
            course_name = serializer.data['name']
            new_course = Course.objects.create(
                name=course_name,
                professor=User.objects.get(pk=request.user.pk)
            )
            d1 = Document.objects.create(course=new_course, name=NAME_ONE,
                                         link=LINK_ONE)
            new_course.document_set.add(d1)
            d2 = Document.objects.create(course=new_course, name=NAME_TWO, link=LINK_TWO)
            new_course.document_set.add(d2)
            new_course.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, format=None, *args, **kwargs):
        '''
        Updating a course - not sure if I will add editing to home course page,
        or if this should be the function to use with the course detail tab,
        not sure if its good to use the same view for two different templates
        and js files either.
        '''
        # print request.DATA
        serializer = CompleteCourseSerializer(data=request.DATA)
        if serializer.is_valid():
            course_name = serializer.data['name']
            new_course = Course.objects.create(
                name=course_name,
                professor=User.objects.get(pk=request.user.pk))
            new_course.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None, *args, **kwargs):
        '''
        Admin wishes to delete a course - perhaps well just
        have it marked as archived?
        '''
        dc = Course.objects.get(pk=pk)
        dc.delete()
        try:
            dc = Course.objects.get(pk=pk)
            if dc:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class UserCourseView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        this_user = User.objects.get(pk=request.user.pk)
        courses = Course.objects.filter(professor=this_user)
        serializer = CourseNameIDSerializer(courses, many=True)
        return Response(serializer.data)


class AllCourseView(APIView):
    '''
    Does the current layout even make sense? The admin can see all courses,
    but teachers can't see a list of their courses or all courses? What is
    the purpose to 2 different lists if there are not that many courses?
    '''
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        courses = Course.objects.all()
        serializer = CourseNameIDSerializer(courses, many=True)
        return Response(serializer.data)


class UpdateCourseView(APIView):
    '''
    For now I think it is best to have a separate view for the
    course detail template.
    '''
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Should probably retrieve the information for the course here
        so it appears in the form/prepopulates the fields.
        '''
        course = self.get_object(pk)
        document_list = Document.objects.filter(course=course)
        serializer = CompleteDocumentSerializer(document_list)
        return Response(serializer.data)

    def update(self, request, pk, format=None, *args, **kwargs):
        '''
        For now I am sticking with Backbone convention of using update
        for editing and post for creating.
        '''
        serializer = CompleteCourseSerializer(data=request.DATA)
        '''Also what exactly does is_valid do?'''
        if serializer.is_valid():
            '''There must be some way to automatically update a model?'''
            course = self.get_object(pk)
            course_name = serializer.data['name']
            password = serializer.data['password']
            startingBudget = serializer.data['startingBudget']
            enableNarrative = serializer.data['enableNarrative']
            message = serializer.data['message']
            active = serializer.data['active']
            professor = serializer.data['professor']
            course.name = course_name
            course.password = password
            course.startingBudget = startingBudget
            course.enableNarrative = enableNarrative
            course.message = message
            course.active = active
            course.professor = professor
            course.save()
        return Response(serializer.data)


class ActivateCourseView(APIView):
    '''
    For now I think it is best to have a separate view for the
    course detail template.
    '''
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None, *args, **kwargs):
        '''
        For now I am sticking with Backbone convention of using put
        for editing and post for creating.
        '''
        course = Course.objects.get(pk=pk)
        if course.visible is True:
            course.visible = False
        elif course.visible is False:
            course.visible = True
        course.save()
        serializer = CompleteDocumentSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DocumentView(APIView):
    """
    This view interacts with backbone to allow instructors to
    interact with documents, they can make them available to
    students or revoke them so they are invisible.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        print "Inside GET"
        course = self.get_object(pk)
        print course.document_set.all()
        documents = Document.objects.filter(course=course)
        print documents
        serializer = CompleteDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None, *args, **kwargs):
        document = Document.objects.get(pk=pk)
        if document.visible is True:
            document.visible = False
        elif document.visible is False:
            document.visible = True
        document.save()
        serializer = CompleteDocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherHomeView(DetailView):

    model = UserProfile
    template_name = 'main/instructor/instructor_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(TeacherHomeView, self).dispatch(*args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(TeamHomeView, self).get_context_data(**kwargs)
#         context['user_courses'] = Course.objects.filter(creator=request.user)
#         context['all_courses'] = Course.objects.all()
#         return context


class TeacherCourseDetail(DetailView):
    model = Course
    template_name = 'main/instructor/course_home.html'
    success_url = '/'


class AddStudentView(APIView):
    """
    This view interacts with backbone, lists all students
    in course to allow instructors to add a student to their course.
    """

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        course = self.get_object(pk)
        student_list = UserProfile.objects.filter(course=course)
        serializer = StudentsInCourseSerializer(student_list)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AddStudentToCourseSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, format=None, *args, **kwargs):
        pass

    def delete(self, request, format=None, *args, **kwargs):
        pass


class ListCourseStudentsView(APIView):
    """
    This view interacts with backbone to allow instructors to
    view and edit students to their course.
    """
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        course = self.get_object(pk)
        student_list = UserProfile.objects.filter(course=course)
        serializer = StudentsInCourseSerializer(student_list)
        return Response(serializer.data)


class TeamView(APIView):
    """
    This view interacts with backbone to allow instructors to
    interact with documents, they can make them available to
    students or revoke them so they are invisible.
    """
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        I assume there is a way to also return the
        users of each team with the teams...
        '''
        course = self.get_object(pk)
        team_list = Team.objects.filter(course=course)
        serializer = TeamSerializer(team_list)
        return Response(serializer.data)


'''I am using this view to play around with getting the
flash to run'''


class BrownfieldDemoView(XMLResponseMixin, View):
    '''Initial view/controller uses templates play, bfaxml
    think like in ssnm it has one page and a second call to the flash app
    base template: play
    over template bfaxml

    Added xmlns="http://www.w3.org/1999/xhtml"
    xmlns:py="http://purl.org/kid/ns#"
    to html header - not sure if I need it
    '''
    template_name = 'main/flvplayer.html'
    success_url = '/'

    def get(self, request):
        print "inside get"
        # print type(DEMO_XML)
        # print type(self.render_to_xml_response(DEMO_XML))
        # return self.render_to_xml_response(DEMO_XML)
        # return render(request, 'main/flvplayer.html',
        # content_type="application/xhtml+xml")
        return render(request, 'main/flvplayer.html')


class DemoHomeView(JSONResponseMixin, View):
    '''Again I'm just using this view to get the Flash working,
    no permissions or users'''
    pass
#     def get(self, request, *args, **kwargs):  # , *args, **kwargs):
#         print request.GET
#         country_id = kwargs.pop('country_id', None)
#         country = get_object_or_404(Country, name=country_id)
#
#         schools = []
#         for school in School.objects.filter(country=country):
#             schools.append({'id': str(school.id), 'name': school.name})
#
#         return self.render_to_json_response({'schools': schools})


class DemoHistoryView(APIView):
    """
    A view that returns the XML.
    """
    renderer_classes = (XMLRenderer)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        print "inside demo history get"
        content = {'demo': DEMO_XML}
        return Response(content)


def get_demo(request):
    print "get demo"
    print HttpResponse(INITIAL_XML, mime_type='application/xml')
    return HttpResponse(INITIAL_XML, content_type="application/xhtml+xml")

    # return render(request, 'main/flvplayer.html', {'demo': DEMO_XML},
    # content_type="application/xhtml+xml")
#    return render(request, 'main/flvplayer.html',
#            content_type="application/xhtml+xml")
#    return HttpResponse(DEMO_XML)
#    #return render(request, 'main/flvplayer.html', {'demo': DEMO_XML},
# content_type="application/xhtml+xml")


def get_bfa(request):
    '''Flash is making calls to demo/media/flash/bfa.swf
    so we will give it'''

    print request.GET
    return render(request, 'main/bfa.swf',
                  content_type="application/xhtml+xml")


def get_demo_history(request):
    print "made it to method"
    return HttpResponse(DEMO_XML, content_type="application/xhtml+xml")


def get_demo_info(request):
    return HttpResponse(DEMO_XML)


def get_demo_test(request):
    return HttpResponse("<data><response>OK</response></data>")


def demo_save(request):
    return HttpResponse("<data><response>OK</response></data>")


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
        return super(TeamHomeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeamHomeView, self).get_context_data(**kwargs)
        context['user_courses'] = Course.objects.filter()
        context['all_courses'] = Course.objects.all()
        # context['course_form'] = CourseForm()
        context['documents'] = Document.objects.all()
        return context


class TeamPerformTest(LoggedInMixin, JSONResponseMixin, View):
    pass


class OnLoad(LoggedInMixin, JSONResponseMixin, View):
    pass


class OnSave(LoggedInMixin, JSONResponseMixin, View):
    pass

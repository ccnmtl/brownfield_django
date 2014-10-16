import json
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from django.template import loader
from django.template.context import Context
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import XMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from brownfield_django.main.document_links import NAME_1, \
    LINK_1, NAME_2, LINK_2, NAME_3, LINK_3, NAME_4, LINK_4, \
    NAME_5, LINK_5, NAME_6, LINK_6, NAME_7, LINK_7, NAME_8, LINK_8
from brownfield_django.main.forms import CreateAccountForm
from brownfield_django.main.models import Course, UserProfile, Document, Team
from brownfield_django.main.serializers import AddCourseByNameSerializer, \
    CompleteDocumentSerializer, \
    UserSerializer, TeamNameSerializer, CourseSerializer, OtherUserSerializer
from brownfield_django.main.xml_strings import DEMO_XML, INITIAL_XML
from brownfield_django.mixins import LoggedInMixin, JSONResponseMixin, \
    XMLResponseMixin


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned courses
        filtering against the request.user
        excluding against an `exclude_username` query parameter in the URL.
        """
        if self.request.user.profile.is_student():
            return Course.objects.none()

        queryset = Course.objects.filter(archive=False)

        if self.request.user.profile.is_teacher():
            return queryset.filter(professor=self.request.user)

        if self.request.user.profile.is_admin():
            exclude = self.request.QUERY_PARAMS.get('exclude_username', None)
            if exclude is not None:
                queryset = queryset.exclude(professor__username=exclude)
            else:
                queryset = queryset.filter(professor=self.request.user)

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.profile.is_student():
            return User.objects.get(id=self.request.user.id)
        else:
            return User.objects.all()


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
        '''Using course id from url to retrieve documents.'''
        course = self.get_object(pk)
        documents = Document.objects.filter(course=course)
        serializer = CompleteDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None, *args, **kwargs):
        '''
        We are sending pk of document since it is already associated
        with the course it belongs to.
        '''
        document = Document.objects.get(pk=pk)
        if document.visible is True:
            document.visible = False
        elif document.visible is False:
            document.visible = True
        document.save()
        serializer = CompleteDocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        course_name = request.DATA['name']
        new_course = Course.objects.create(
            name=course_name,
            professor=User.objects.get(pk=request.user.pk)
        )
        d1 = Document.objects.create(course=new_course, name=NAME_1,
                                     link=LINK_1)
        d2 = Document.objects.create(course=new_course, name=NAME_2,
                                     link=LINK_2)
        d3 = Document.objects.create(course=new_course, name=NAME_3,
                                     link=LINK_3)
        d4 = Document.objects.create(course=new_course, name=NAME_4,
                                     link=LINK_4)
        d5 = Document.objects.create(course=new_course, name=NAME_5,
                                     link=LINK_5)
        d6 = Document.objects.create(course=new_course, name=NAME_6,
                                     link=LINK_6)
        d7 = Document.objects.create(course=new_course, name=NAME_7,
                                     link=LINK_7)
        d8 = Document.objects.create(course=new_course, name=NAME_8,
                                     link=LINK_8)
        new_course.document_set.add(d1, d2, d3, d4, d5, d6, d7, d8)
        new_course.save()
        print new_course.document_set.all()
        professor = User.objects.get(pk=request.user.pk)
        new_course = Course.objects.get(
            name=request.DATA['name'],
            professor=professor)
        serializer = AddCourseByNameSerializer(new_course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminStudentView(APIView):
    """
    This view interacts with backbone to allow instructors to
    view and edit students to their course, pk is for course.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None, *args, **kwargs):
        '''Retrieve students of course if there are any to list.'''
        course = self.get_object(pk)
        try:
            students = course.get_students()
            users = User.objects.filter(profile__in=students)
            serializer = OtherUserSerializer(users, many=True)
            return Response(serializer.data)
        except:
            '''Assume collection is currently empty'''
            return Response(status.HTTP_200_OK)

    def post(self, request, pk, format=None, *args, **kwargs):
        '''
        Add a Student
        Get course to associate with student and save, both in json.
        '''
        course = self.get_object(pk)
        first_name = request.DATA['first_name']
        last_name = request.DATA['last_name']
        email = request.DATA['email']
        ini = first_name[0]
        username = str(ini) + str(last_name)
        new_user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            last_name=last_name)
        new_user.email = email
        new_user.save()
        new_profile = UserProfile.objects.create(course=course,
                                                 user=new_user,
                                                 profile_type='ST')
        new_profile.save()
        serializer = OtherUserSerializer(data=new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminTeamView(APIView):
    """
    This view interacts with backbone to allow instructors to
    view and add teams to their course. Will also probably be where
    logic for keeping track of which students are where will be.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None, *args, **kwargs):
        '''Send back all teams currently in course.'''
        course = self.get_object(pk)
        try:
            teamprofiles = course.get_teams()
            teams = User.objects.filter(team__in=teamprofiles)
            serializer = TeamNameSerializer(teams, many=True)
            return Response(serializer.data)
        except:
            '''Assume collection is currently empty'''
            return Response(status.HTTP_200_OK)

    def post(self, request, pk, format=None, *args, **kwargs):
        '''
        Add a team.
        Team creation is where we set the team
        budgets so they are all the same.
        '''
        course = self.get_object(pk)
        team_name = request.DATA['username']
        password1 = request.DATA['password1']
        password2 = request.DATA['password2']
        if password1 == password2:
            user = User.objects.create_user(username=team_name,
                                            first_name=team_name,
                                            password=password1)
            team = Team.objects.create(
                user=user,
                course=course,
                budget=course.startingBudget,
                team_passwd=password1)
            team.save()  # saving bc pylint complains it is not used
            try:
                new_user = User.objects.get(username=team_name)
                serializer = TeamNameSerializer(new_user)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except:
                print 'could not find user'
        else:
            print "passwords do not match"
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class HomeView(LoggedInMixin, View):
    '''redoing so that it simply redirects people where they need to be'''

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user.pk)
        except UserProfile.DoesNotExist:
            return HttpResponseRedirect(reverse('register'))

        if user_profile.is_teacher():
            url = '/teacher/home/%s/' % (user_profile.id)
        if user_profile.is_admin():
            url = '/ccnmtl/home/%s/' % (user_profile.id)

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


class DetailJSONCourseView(JSONResponseMixin, View):
    '''
    For now I think it is best to have a separate view for the
    course detail template.
    '''

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def convert_TF_to_json(self, attribute):
        if attribute is True:
            return 'true'
        elif attribute is False:
            return 'false'

    def convert_TF_from_json(self, attribute):
        if attribute == 'true':
            return True
        elif attribute == 'false':
            return False

    def get(self, request, pk, format=None, *args, **kwargs):
        '''
        Should probably retrieve the information for the course here
        so it appears in the form/pre-populates the fields.
        '''
        course = self.get_object(pk)
        j_course = []
        j_course.append({'id': str(course.id),
                         'name': course.name,
                         'startingBudget': course.startingBudget,
                         'enableNarrative': self.convert_TF_to_json(
                             course.enableNarrative),
                         'message': course.message,
                         'active': self.convert_TF_to_json(course.active),
                         'archive': self.convert_TF_to_json(course.archive),
                         'professor': str(course.professor)
                         })
        return self.render_to_json_response({'course': j_course})

    def post(self, request, pk, format=None, *args, **kwargs):
        '''This is really really ugly as is get method need to clean up.'''
        course = self.get_object(pk)
        course.name = self.request.POST.get('name')
        course.startingBudget = int(self.request.POST.get('startingBudget'))
        course.enableNarrative = self.convert_TF_from_json(
            self.request.POST.get('enableNarrative'))
        course.message = self.request.POST.get('message')
        course.active = self.convert_TF_from_json(
            self.request.POST.get('active'))
        course.archive = self.convert_TF_from_json(
            self.request.POST.get('archive'))
        userprof = User.objects.get(
            username=self.request.POST.get('professor'))
        course.professor = userprof
        course.save()
        j_course = []
        j_course.append({'id': str(course.id),
                         'name': course.name,
                         'startingBudget': course.startingBudget,
                         'enableNarrative': self.convert_TF_to_json(
                             course.enableNarrative),
                         'message': course.message,
                         'active': self.convert_TF_to_json(course.active),
                         'archive': self.convert_TF_to_json(course.archive),
                         'professor': str(course.professor)
                         })
        return self.render_to_json_response({'course': j_course})


class ActivateCourseView(JSONResponseMixin, View):
    '''
    This should be a FormView but not sure how to do variable # of arguments,
    going to hack out to have working for now...
    '''

    def send_student_email(self, student):
        template = loader.get_template(
            'main/ccnmtl/course_activation/student_activation_notice.txt')
        subject = "Welcome to Brownfield!"
        ctx = Context({'student': student, 'team': student.profile.team})
        message = template.render(ctx)
        '''who is the sender?'''
        sender = 'cdunlop@columbia.edu'  # settings.BNFD_MAIL
        send_mail(subject, message, sender, [student.email])

    def post(self, request, pk):
        '''This is really really ugly as is get method need to clean up.'''
        student_list = json.loads(request.POST['student_list'])
        for student in student_list:
            team = Team.objects.get(pk=student['student']['team_id'])
            student = User.objects.get(pk=student['student']['pk'])
            profile = UserProfile.objects.get(user=student)
            team.userprofile_set.add(profile)
            self.send_student_email(student)
        act_crs = Course.objects.get(pk=pk)
        act_crs.active = True
        act_crs.save()
        return self.render_to_json_response({'success': 'true'})


class CreateTeamsView(DetailView):
    """
    Until I figure out nested views in Backbone or some Backbone plug-in...
    Having one page with drop downs to add students to teams
    """
    model = Course
    template_name = 'main/ccnmtl/course_activation/create_teams.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CreateTeamsView, self).get_context_data(**kwargs)
        context['team_list'] = self.object.get_teams()
        context['student_list'] = User.objects.filter(
            profile__in=self.object.get_students())
        return context


class EditCourseTeamsView(View):

    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        course.active = False
        url = '../../create_teams/' + str(course.pk) + '/'
        return HttpResponseRedirect(url)


class TeacherHomeView(DetailView):

    model = UserProfile
    template_name = 'main/ccnmtl/home_dash/ccnmtl_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(TeacherHomeView, self).dispatch(*args, **kwargs)


class TeacherCourseDetail(DetailView):

    model = Course
    template_name = 'main/instructor/course_dash/course_home.html'
    success_url = '/'


class CCNMTLHomeView(DetailView):

    model = UserProfile
    template_name = 'main/ccnmtl/home_dash/ccnmtl_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(CCNMTLHomeView, self).dispatch(*args, **kwargs)


class CCNMTLCourseDetail(DetailView):

    model = Course
    template_name = 'main/ccnmtl/course_dash/course_home.html'
    success_url = '/'


class CCNMTLViewTeamsDetail(DetailView):

    model = Course
    template_name = 'main/ccnmtl/course_activation/teams.html'
    success_url = '/'

#     def get_context_data(self, **kwargs):
#         context = super(CreateTeamsView, self).get_context_data(**kwargs)
#         context['team_list'] = User.objects.filter(
#             profile__in=self.object.get_teams())
#         context['student_list'] = User.objects.filter(
#             profile__in=self.object.get_students())
#         return context


'''Beginning of Team Views'''


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
    model = UserProfile
    template_name = 'main/team/team_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(TeamHomeView, self).dispatch(*args, **kwargs)


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


class TeamPerformTest(LoggedInMixin, JSONResponseMixin, View):
    pass


class OnLoad(LoggedInMixin, JSONResponseMixin, View):
    pass


class OnSave(LoggedInMixin, JSONResponseMixin, View):
    pass

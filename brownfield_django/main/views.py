import csv
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template import loader
from django.template.context import Context
from django.views.generic import View
from django.views.generic.detail import DetailView

from rest_framework import status, viewsets
from rest_framework.response import Response

from brownfield_django.main.models import Course, UserProfile, Document, \
    Team, History, Information, PerformedTest
from brownfield_django.main.serializers import DocumentSerializer, \
    UserSerializer, TeamUserSerializer, CourseSerializer, \
    StudentUserSerializer, StudentMUserSerializer, InstructorSerializer
from brownfield_django.main.xml_strings import INITIAL_XML
from brownfield_django.mixins import LoggedInMixin, JSONResponseMixin, \
    CSRFExemptMixin, PasswordMixin, UniqUsernameMixin, \
    LoggedInMixinAdminInst, LoggedInMixinAdministrator


class CourseViewSet(LoggedInMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned courses
        filtering against the request.user
        excluding against an `exclude_username` query parameter in the URL.
        """
        queryset = Course.objects.none()

        if self.request.user.profile.is_student():
            queryset = Course.objects.none()
        elif self.request.user.profile.is_teacher():
            queryset = Course.objects.filter(
                professor=self.request.user).order_by('name')
        elif self.request.user.profile.is_admin():
            queryset = Course.objects.filter(archive=False).order_by('name')
        return queryset


class DocumentViewSet(LoggedInMixin, viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        '''
        Form Docs: queryset that should be used for list views,
        and that should be used as the base for lookups in detail views.
        '''
        course_pk = self.request.query_params.get('course', None)
        doc_pk = self.kwargs.get('pk', None)
        up = self.request.user.profile
        queryset = Document.objects.none()

        if up.is_student():
            queryset = Document.objects.none()
        elif up.is_admin() or up.is_teacher():
            if course_pk is not None:
                queryset = Document.objects.filter(course__pk=course_pk)
            elif doc_pk is not None:
                queryset = Document.objects.filter(pk=doc_pk)
        return queryset


class UserViewSet(LoggedInMixin, viewsets.ModelViewSet):
    '''This is for the main page with the list of the users courses
    it is not for viewing team users or student users, only users who should
    see a complete list of instructors are admins'''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all().order_by('username')
        if self.request.user.profile.is_admin():
            return queryset
        else:
            return queryset.filter(id=self.request.user.id)


class StudentViewSet(LoggedInMixin, UniqUsernameMixin, viewsets.ModelViewSet):
    '''Attempting to redo Student Ajax handling
    the correct way with a model viewset - still very wrong.'''
    queryset = User.objects.filter(profile__profile_type='ST')
    serializer_class = StudentUserSerializer

    def create(self, request):
        up = self.request.user.profile
        if up.is_teacher() or up.is_admin():
            try:
                key = self.request.query_params.get('course', None)
                course = Course.objects.get(pk=key)
                '''want to check for extremely rare occurrence that user
                may already exist or the name is too long.'''
                uniq_name = self.get_unique_username(
                    str(request.data['first_name']),
                    str(request.data['last_name']))
                student = User.objects.create_user(
                    username=uniq_name,
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'],
                    email=request.data['email'])
                new_profile = UserProfile.objects.create(course=course,
                                                         user=student,
                                                         profile_type='ST')
                new_profile.save()
                serializer = StudentMUserSerializer(student)
                return Response(serializer.data, status.HTTP_201_CREATED)
            except:
                # is it considered good practice to return serializer.data
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        up = self.request.user.profile
        student = get_object_or_404(User, pk=pk)
        if up.is_teacher() or up.is_admin():
            try:
                # should I be sticking this in StudentMUserSerializer
                student.first_name = request.data['first_name']
                student.last_name = request.data['last_name']
                student.email = request.data['email']
                student.save()
                return Response(
                    status=status.HTTP_200_OK)
            except:
                '''For some reason update failed'''
                return Response({"success": False})
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        course_pk = self.request.query_params.get('course', None)
        usr_pk = self.kwargs.get('pk', None)
        up = self.request.user.profile

        if course_pk is not None and (up.is_teacher() or up.is_admin()):
            students = UserProfile.objects.filter(course__pk=course_pk,
                                                  profile_type='ST')
            queryset = User.objects.filter(
                profile__in=students).order_by('first_name')
        elif usr_pk is not None and (up.is_teacher() or up.is_admin()):
            # doesn't seem to like .get but .filter is
            queryset = User.objects.filter(pk=usr_pk)
        else:
            '''Assume there are no students or user is unauthorized.'''
            queryset = User.objects.none()
        return queryset


class InstructorViewSet(LoggedInMixin, UniqUsernameMixin,
                        PasswordMixin, viewsets.ModelViewSet):
    '''This could probably be combined with StudentViewSet
    not sure though.'''
    queryset = User.objects.filter(
        profile__profile_type='TE').filter(profile__archive=False)
    serializer_class = InstructorSerializer

    def send_instructor_email(self, instructor, profile):
        '''Send instructor their credentials'''
        template = loader.get_template(
            'main/ccnmtl/course_dash/instructor_activation_notice.txt')
        subject = "Welcome to Brownfield!"
        ctx = Context({'instructor': instructor,
                       'profile': profile,
                       'site': Site.objects.get_current()})
        message = template.render(ctx)
        '''who is the sender?'''
        sender = settings.SERVER_EMAIL
        send_mail(subject, message, sender, [instructor.email])

    def create(self, request):
        '''Since there is no course associated we can
        see about saving the serializer directly'''
        up = self.request.user.profile
        if up.is_student() or up.is_teacher():
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif up.is_admin():
            try:
                '''want to check for extremely rare occurrence that user
                may already exist or the name is too long.'''
                uniq_name = self.get_unique_username(
                    str(request.data['first_name']),
                    str(request.data['last_name']))
                instructor = User.objects.create_user(
                    username=uniq_name,
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'],
                    email=request.data['email'])
                tmpasswd = self.get_password()
                instructor.set_password(tmpasswd)
                instructor.save()
                new_profile = UserProfile.objects.create(user=instructor,
                                                         profile_type='TE')
                new_profile.tmp_passwd = tmpasswd
                new_profile.save()
                self.send_instructor_email(instructor, new_profile)
                serializer = StudentMUserSerializer(instructor)
                return Response(serializer.data, status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        up = self.request.user.profile
        if up.is_student() or up.is_teacher():
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif up.is_admin():
            instructor = get_object_or_404(User, pk=pk)
            serializer = InstructorSerializer(
                instructor, data=request.data, partial=True)
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data, status.HTTP_200_OK)
                except:
                    '''For some reason update failed'''
                    return Response({"success": False})
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        up = self.request.user.profile
        queryset = User.objects.none()
        if up.is_admin():
            instructors = UserProfile.objects.filter(
                profile_type='TE').filter(archive=False)
            queryset = User.objects.filter(profile__in=instructors)
        return queryset


class TeamViewSet(LoggedInMixin, PasswordMixin, viewsets.ModelViewSet):
    '''Finally moving team to viewset instead of API View'''
    team_set = Team.objects.all()
    queryset = User.objects.filter(team__in=team_set)
    serializer_class = TeamUserSerializer

    def create(self, request):
        up = self.request.user.profile
        if up.is_teacher() or up.is_admin():
            try:
                key = self.request.query_params.get('course', None)
                course = Course.objects.get(pk=key)
                team_name = request.data['team_name']
                '''If team name is blank, make something up'''
                if team_name == '':
                    team_name = "team"
                '''creating team with no attributes first so we can
                create a unique username for user based on team pk'''
                team = Team.objects.create(course=course,
                                           budget=course.startingBudget)
                user = User.objects.create(username=team_name + "_" +
                                           str(team.pk))
                user.first_name = team_name
                tmpasswd = self.get_password()
                user.set_password(tmpasswd)
                team.user = user
                team.team_passwd = tmpasswd
                team.save()
                user.save()
                serializer = TeamUserSerializer(user)
                return Response(serializer.data, status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        '''Send back all teams currently in course.'''
        course_pk = self.request.query_params.get('course', None)
        team_pk = self.kwargs.get('pk', None)
        up = self.request.user.profile

        if course_pk is not None and (up.is_teacher() or up.is_admin()):
            course = Course.objects.get(pk=course_pk)
            teamprofiles = course.get_teams()
            queryset = User.objects.filter(team__in=teamprofiles)
            return queryset
        if team_pk is not None and (up.is_teacher() or up.is_admin()):
            queryset = User.objects.filter(pk=team_pk)
            return queryset
        else:
            queryset = User.objects.none()
        return queryset


class HomeView(LoggedInMixin, View):
    '''redoing so that it simply redirects people where they need to be'''

    def get(self, request):
        url = '/'
        try:
            user_profile = UserProfile.objects.get(user=request.user.pk)
            url = user_profile.get_absolute_url()
        except UserProfile.DoesNotExist:
            try:
                '''First see if user is in 'tlc.cunix.local:columbia.edu'
                group'''
                if (request.user.groups.filter(
                        name='tlc.cunix.local:columbia.edu').count() > 0):
                            up = UserProfile.objects.create(user=request.user,
                                                            profile_type='AD')
                            up.save()
                else:
                    team = Team.objects.get(user=request.user.pk)
                    url = '/team/home/%s/' % (team.id)
            except:
                pass
        return HttpResponseRedirect(url)


class ArchiveCourseView(LoggedInMixin, LoggedInMixinAdminInst,
                        JSONResponseMixin, View):

    def get(self, request, pk):
        crs = Course.objects.get(pk=pk)
        crs.archive = True
        crs.save()
        return self.render_to_json_response({'success': 'true'})


class ActivateCourseView(LoggedInMixin, LoggedInMixinAdminInst,
                         JSONResponseMixin, View):

    def send_student_email(self, student):
        '''Should instructors be sent
        emails saying their class is activated?'''
        template = loader.get_template(
            'main/ccnmtl/course_dash/student_activation_notice.txt')
        subject = "Welcome to Brownfield!"
        ctx = Context({'student': student,
                       'team': student.profile.team,
                       'site': Site.objects.get_current()})
        message = template.render(ctx)
        '''who is the sender?'''
        sender = settings.SERVER_EMAIL
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


class EditTeamsView(LoggedInMixin, LoggedInMixinAdminInst, View):

    def get(self, request, pk):
        template = loader.get_template(
            'main/ccnmtl/course_dash/team_form.html')
        course = Course.objects.get(pk=pk)
        ctx = Context({'object': course})
        edit_template = template.render(ctx)
        return HttpResponse(edit_template)


class ShowTeamsView(LoggedInMixin, LoggedInMixinAdminInst, View):

    def get(self, request, pk):
        template = loader.get_template(
            'main/ccnmtl/course_dash/team_table.html')
        course = Course.objects.get(pk=pk)
        ctx = Context({'object': course})
        edit_template = template.render(ctx)
        return HttpResponse(edit_template)


class ShowProfessorsView(LoggedInMixin, LoggedInMixinAdministrator, View):

    def get(self, request):
        template = loader.get_template(
            'main/ccnmtl/home_dash/instructor_list.html')
        profiles = UserProfile.objects.filter(profile_type='TE')
        professors = User.objects.filter(profile__in=profiles)
        ctx = Context({'professors': professors})
        edit_template = template.render(ctx)
        return HttpResponse(edit_template)


class CCNMTLHomeView(LoggedInMixin, LoggedInMixinAdminInst, DetailView):

    model = UserProfile
    template_name = 'main/ccnmtl/home_dash/ccnmtl_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(CCNMTLHomeView, self).dispatch(*args, **kwargs)


class CCNMTLCourseDetail(LoggedInMixin, LoggedInMixinAdminInst, DetailView):

    model = Course
    template_name = 'main/ccnmtl/course_dash/course_home.html'
    success_url = '/'


'''CCNMTL/Admin Interactive Views'''


class BrownfieldInfoView(CSRFExemptMixin, View):
    '''Corresponds to "demo/info/"'''
    def get(self, request):
        if request.user.profile.is_admin():
            return HttpResponse("<data><response>OK</response></data>")
        elif request.user.profile.is_teacher():
            '''This may need to be changed...'''
            return HttpResponse(INITIAL_XML)

    def post(self, request):
        if request.user.profile.is_admin():
            return HttpResponse("<data><response>OK</response></data>")
        elif request.user.profile.is_teacher():
            '''This may need to be changed...'''
            return HttpResponse("<data><response>OK</response></data>")


class BrownfieldHistoryView(CSRFExemptMixin, View):

    def get(self, request):
        if request.user.profile.is_admin():
            return HttpResponse(INITIAL_XML)
        elif request.user.profile.is_teacher():
            '''This may need to be changed...'''
            return HttpResponse(INITIAL_XML)

    def post(self, request):
        if request.user.profile.is_admin():
            return HttpResponse(INITIAL_XML)
        elif request.user.profile.is_teacher():
            '''This may need to be changed...'''
            return HttpResponse(INITIAL_XML)


class BrownfieldTestView(CSRFExemptMixin, View):

    def get(self, request):
        if request.user.profile.is_admin():
            return HttpResponse(INITIAL_XML)
        elif request.user.profile.is_teacher():
            '''This may need to be changed...'''
            return HttpResponse(INITIAL_XML)

    def post(self, request):
        if request.user.profile.is_admin():
            return HttpResponse(INITIAL_XML)
        elif request.user.profile.is_teacher():
            '''This may need to be changed...'''
            return HttpResponse(INITIAL_XML)


'''Beginning of Team Views'''


class TeamHomeView(LoggedInMixin, DetailView):

    model = Team
    template_name = 'main/team/team_home.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if (self.request.user.is_anonymous() or
                (int(kwargs.get('pk')) != self.request.user.team.id)):
            return HttpResponseForbidden("forbidden")
        return super(TeamHomeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeamHomeView, self).get_context_data(**kwargs)
        course = Course.objects.get(pk=self.object.course.pk)
        context['document_list'] = course.document_set.filter(visible=True)
        return context


"""Team Views for interactive."""


class TeamHistoryView(CSRFExemptMixin, View):
    """Need to parse the XML and substitute the correct
    values for each student interaction."""

    def initial_team_history(self, team):
        template = loader.get_template(
            'main/team/history.txt')
        ctx = Context({'team': team})
        xml_history = template.render(ctx)
        return xml_history

    def send_team_history(self, team):
        template = loader.get_template(
            'main/team/bfaxml.txt')
        history = History.objects.filter(team=team)
        team_info = Information.objects.filter(history=history)
        tests_perf = PerformedTest.objects.filter(history=history)

        ctx = Context({'team': team, 'team_info': team_info,
                       'team_tests': tests_perf, 'team_history': history})
        xml_history = template.render(ctx)
        return xml_history

    def get(self, request, pk):
        """Get retrieves the current team values for the flash."""
        team = Team.objects.get(user=request.user)
        chk_history = History.objects.filter(team=team)

        if chk_history.count() == 0:
            return HttpResponse(self.initial_team_history(team))
        elif chk_history.count() > 0:
            return HttpResponse(self.send_team_history(team))


class TeamInfoView(CSRFExemptMixin, View):

    def post(self, request, pk):
        team = Team.objects.get(user=request.user)
        infoType = request.POST['infoType']

        if infoType == "recon":
            th = History.objects.create(
                team=team,
                date=request.POST['date'],
                description=request.POST['description'],
                cost=request.POST['cost'])
            inf = Information.objects.create(
                history=th,
                infoType=request.POST['infoType'],
                internalName=request.POST['internalName'])
            return HttpResponse("<data><response>OK</response></data>")

        elif infoType == "visit":
            th = History.objects.create(
                team=team,
                date=request.POST['date'],
                description=request.POST['description'],
                cost=request.POST['cost'])
            th.save()
            inf = Information.objects.create(
                history=th,
                internalName=request.POST['internalName'],
                infoType=request.POST['infoType'])
            return HttpResponse("<data><response>OK</response></data>")

        elif infoType == "question":
            th = History.objects.create(
                team=team,
                date=request.POST['date'],
                description=request.POST['description'],
                cost=request.POST['cost'])
            inf = Information.objects.create(
                history=th,
                internalName=request.POST['internalName'],
                infoType=request.POST['infoType'])
            return HttpResponse("<data><response>OK</response></data>")

        elif infoType == "doc":
            th = History.objects.create(
                team=team,
                date=request.POST['date'],
                description=request.POST['description'],
                cost=request.POST['cost'])
            inf = Information.objects.create(
                history=th,
                internalName=request.POST['internalName'],
                infoType=request.POST['infoType'])
            inf.save()
            return HttpResponse("<data><response>OK</response></data>")


class TeamPerformTest(CSRFExemptMixin, View):

    def post(self, request, pk):
        team = Team.objects.get(user=request.user)

        th = History.objects.create(
            team=team,
            date=request.POST['date'],
            description=request.POST['description'],
            cost=request.POST['cost'])
        pf = PerformedTest.objects.create(
            history=th,
            x=int(request.POST['x']),
            y=int(request.POST['y']),
            testNumber=int(request.POST['testNumber']))
        try:
            pf.z = request.POST['z']
            pf.save()
        except:
            pass
        try:
            pf.testDetails = request.POST['testDetails']
            pf.save()
        except:
            pass
        try:
            pf.paramString = request.POST['paramString']
            pf.save()
        except:
            pass
        return HttpResponse("<data><response>OK</response></data>")


class TeamCSV(LoggedInMixin, View):

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        team = Team.objects.get(user=user)
        history = History.objects.filter(team=team)

        team_info = Information.objects.filter(history=history)
        tests_perf = PerformedTest.objects.filter(history=history)

        columns = ['Cost', 'Date', 'Description', 'X', 'Y', 'Z']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + \
            str(user.username) + '_' + 'team.course' + '.csv'
        writer = csv.writer(response, dialect='excel')
        writer.writerow(columns)

        for info in team_info:
            columns = [info.history.cost, info.history.date,
                       info.history.description]
            writer.writerow(columns)

        for test in tests_perf:
            if test.testNumber == 5 or test.testNumber == 7:
                columns = [test.history.cost, test.history.date,
                           test.history.description, test.x, test.y, test.z]
            else:
                columns = [test.history.cost, test.history.date,
                           test.history.description, test.x, test.y, 'None']
            writer.writerow(columns)
        return response


class TeamSignContract(LoggedInMixin, JSONResponseMixin, View):

    def post(self, request):
        team = Team.objects.get(user=request.user)
        team.signed_contract = True
        team.save()
        return self.render_to_json_response({'success': 'true'})

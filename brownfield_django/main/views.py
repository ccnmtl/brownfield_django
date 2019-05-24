import csv
import json

from boto.s3.connection import S3Connection
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.flatpages.views import flatpage
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseBadRequest)
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.text import slugify
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
    LoggedInMixinAdminInst, LoggedInMixinAdministrator, ProfileMixin


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
        try:
            up = self.request.user.profile
            if not up.is_teacher() and not up.is_admin():
                return Response(status=status.HTTP_403_FORBIDDEN)

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
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except (Course.DoesNotExist, KeyError, ValueError):
            return Response({"success": False})

    def update(self, request, pk=None):
        try:
            up = self.request.user.profile

            if not up.is_teacher() and not up.is_admin():
                return Response(status=status.HTTP_403_FORBIDDEN)

            student = get_object_or_404(User, pk=pk)

            # should I be sticking this in StudentMUserSerializer
            student.first_name = request.data['first_name']
            student.last_name = request.data['last_name']
            student.email = request.data['email']
            student.save()
            return Response(
                status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except (KeyError, ValueError):
            '''For some reason update failed'''
            return Response({"success": False})

    def get_queryset(self):
        course_pk = self.request.query_params.get('course', None)
        usr_pk = self.kwargs.get('pk', None)

        try:
            up = self.request.user.profile
        except UserProfile.DoesNotExist:
            return User.objects.none()

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
        ctx = {'instructor': instructor,
               'profile': profile,
               'site': Site.objects.get_current()}
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
                serializer = InstructorSerializer(instructor)
                return Response(serializer.data, status.HTTP_201_CREATED)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        up = self.request.user.profile
        if up.is_student() or up.is_teacher():
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif up.is_admin():
            return self.admin_update(request, pk, up)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def admin_update(self, request, pk, up):
        instructor = get_object_or_404(User, pk=pk)
        serializer = InstructorSerializer(
            instructor, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            except ValueError:
                '''For some reason update failed'''
                return Response({"success": False})
        # NOTE: there is no return specified when the serializer
        #       is not valid. This is probably a bug since
        #       the method will return `None`, and that's not
        #       a valid Django response.

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
                # Django uses a 30-character Char field for first_name.
                user.first_name = team_name[:30]
                tmpasswd = self.get_password()
                user.set_password(tmpasswd)
                team.user = user
                team.team_passwd = tmpasswd
                team.save()
                user.save()
                serializer = TeamUserSerializer(user)
                return Response(serializer.data, status.HTTP_201_CREATED)
            except ValueError:
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
            '''First see if user is in admin group'''
            url = self.admin_or_team_url(request.user)
        return HttpResponseRedirect(url)

    def admin_or_team_url(self, user):
        url = '/'
        if (user.groups.filter(name=settings.ADMIN_AFFIL).exists()):
            up = UserProfile.objects.create(user=user, profile_type='AD')
            up.save()
        else:
            try:
                team = Team.objects.get(user=user.pk)
                url = '/team/home/%s/' % (team.pk)
            except Team.DoesNotExist:
                pass
        return url


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
        ctx = {'student': student,
               'team': student.profile.team,
               'site': Site.objects.get_current()}
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
        ctx = {'object': course}
        edit_template = template.render(ctx)
        return HttpResponse(edit_template)


class ShowTeamsView(LoggedInMixin, LoggedInMixinAdminInst, View):

    def get(self, request, pk):
        template = loader.get_template(
            'main/ccnmtl/course_dash/team_table.html')
        course = Course.objects.get(pk=pk)
        ctx = {'object': course}
        edit_template = template.render(ctx)
        return HttpResponse(edit_template)


class ShowProfessorsView(LoggedInMixin, LoggedInMixinAdministrator, View):

    def get(self, request):
        template = loader.get_template(
            'main/ccnmtl/home_dash/instructor_list.html')
        profiles = UserProfile.objects.filter(profile_type='TE')
        professors = User.objects.filter(profile__in=profiles)
        ctx = {'professors': professors}
        edit_template = template.render(ctx)
        return HttpResponse(edit_template)


class CCNMTLHomeView(LoggedInMixin, LoggedInMixinAdminInst,
                     ProfileMixin, DetailView):

    model = UserProfile
    template_name = 'main/ccnmtl/home_dash/ccnmtl_home.html'
    success_url = '/'


class CCNMTLCourseDetail(LoggedInMixin, LoggedInMixinAdminInst, DetailView):

    model = Course
    template_name = 'main/ccnmtl/course_dash/course_home.html'
    success_url = '/'


'''CCNMTL/Admin Interactive Views'''


class BrownfieldDemoView(CSRFExemptMixin, View):
    def get(self, request):
        return HttpResponse(INITIAL_XML)

    def post(self, request):
        return HttpResponse("<data><response>OK</response></data>")


'''Beginning of Team Views'''


class TeamHomeView(LoggedInMixin, DetailView):

    model = Team
    template_name = 'main/team/team_home_html5.html'
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
        ctx = {'team': team}
        xml_history = template.render(ctx)
        return xml_history

    def send_team_history(self, team):
        template = loader.get_template(
            'main/team/bfaxml.txt')
        history = History.objects.filter(team=team)
        team_info = Information.objects.filter(history__id__in=history)
        tests_perf = PerformedTest.objects.filter(history__id__in=history)

        ctx = {'team': team, 'team_info': team_info,
               'team_tests': tests_perf, 'team_history': history}
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


class TeamInfoView(CSRFExemptMixin, LoggedInMixin, View):

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


def all_keys_in_dict(d, keys):
    for k in keys:
        if k not in d:
            return False
    return True


class TeamPerformTest(CSRFExemptMixin, LoggedInMixin, View):

    def validate(self, request):
        required_fields = ['date', 'cost', 'x', 'y', 'testNumber']
        int_fields = ['x', 'y', 'testNumber']
        if not all_keys_in_dict(request.POST, required_fields):
            return False
        for p in int_fields:
            try:
                int(request.POST[p])
            except ValueError:
                return False
        return True

    def post(self, request, pk):
        team = Team.objects.get(user=request.user)
        if not self.validate(request):
            return HttpResponseBadRequest("missing or invalid parameter")

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

        self.save_z(request, pf)
        self.save_test_details(request, pf)
        self.save_param_string(request, pf)

        return HttpResponse("<data><response>OK</response></data>")

    def save_z(self, request, pf):
        try:
            pf.z = request.POST['z']
            pf.save()
        except MultiValueDictKeyError:
            pass

    def save_test_details(self, request, pf):
        try:
            pf.testDetails = request.POST['testDetails']
            pf.save()
        except MultiValueDictKeyError:
            pass

    def save_param_string(self, request, pf):
        try:
            pf.paramString = request.POST['paramString']
            pf.save()
        except MultiValueDictKeyError:
            pass


class TeamCSV(LoggedInMixin, View):

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        team = Team.objects.get(user=user)

        history = History.objects.filter(team=team)
        team_info = Information.objects.filter(history__id__in=history)
        tests_perf = PerformedTest.objects.filter(history__id__in=history)

        columns = ['Cost', 'Date', 'Description', 'X', 'Y', 'Z']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + \
            slugify(user.username) + '_' + 'team.course' + '.csv'
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


class TeamSignContract(LoggedInMixin, View):

    def post(self, request):
        team = Team.objects.get(user=request.user)
        team.signed_contract = True
        team.save()
        return HttpResponseRedirect(self.request.POST.get('next'))


class RestrictedFlatPage(View):

    def get(self, *args, **kwargs):
        if (self.request.user.is_staff or
            (hasattr(self.request.user, 'profile') and
             self.request.user.profile.is_teacher())):
            return flatpage(self.request, self.request.path)

        return HttpResponseRedirect('/')


# based on
# https://www.gyford.com/phil/writing/2012/09/26/django-s3-temporary/
class RestrictedFile(View):
    permanent = False

    def get_signed_url(self):
        s3 = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        path = '/uploads/instructors/{}'.format(self.kwargs['path'])

        # Create a URL valid for 5 minutes
        return s3.generate_url(
            300, 'GET', bucket=settings.AWS_STORAGE_BUCKET_NAME,
            key=path)

    def get(self, *args, **kwargs):
        url = '/'
        if (self.request.user.is_staff or
            (hasattr(self.request.user, 'profile') and
             self.request.user.profile.is_teacher())):
            url = self.get_signed_url()

        return HttpResponseRedirect(url)

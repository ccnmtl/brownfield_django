import json
import random
from string import ascii_letters, digits

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http.response import HttpResponseNotAllowed, HttpResponse, \
    HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from brownfield_django.main.models import UserProfile


def ajax_required(func):
    """
    AJAX request required decorator
    use it in your views:
    @ajax_required
    def my_view(request):
    """

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseNotAllowed("")
        return func(request, *args, **kwargs)

    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap


def instructor_or_admin(user):
    try:
        return user.profile.is_admin() or user.profile.is_teacher()
    except UserProfile.DoesNotExist:
        return False


def user_is_admin(user):
    try:
        return user.profile.is_admin()
    except UserProfile.DoesNotExist:
        return False


class JSONResponseMixin(object):
    @method_decorator(ajax_required)
    def dispatch(self, *args, **kwargs):
        return super(JSONResponseMixin, self).dispatch(*args, **kwargs)

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(json.dumps(context),
                            content_type='application/json',
                            **response_kwargs)


class CSRFExemptMixin(object):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class LoggedInMixinStaff(object):
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixinStaff, self).dispatch(*args, **kwargs)


class LoggedInMixinSuperuser(object):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixinSuperuser, self).dispatch(*args, **kwargs)


class LoggedInMixinAdminInst(object):
    @method_decorator(
        user_passes_test(
            instructor_or_admin, login_url=None, redirect_field_name=None))
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixinAdminInst, self).dispatch(*args, **kwargs)


class LoggedInMixinAdministrator(object):
    @method_decorator(
        user_passes_test(
            user_is_admin, login_url=None, redirect_field_name=None))
    def dispatch(self, *args, **kwargs):
        return super(
            LoggedInMixinAdministrator, self).dispatch(*args, **kwargs)


class ProfileMixin(object):

    def dispatch(self, *args, **kwargs):
        if int(kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseForbidden("forbidden")
        return super(ProfileMixin, self).dispatch(*args, **kwargs)


class PasswordMixin(object):

    def get_password(self):
        char_digits = ascii_letters + digits
        self.passwd = ''
        for x in range(0, 7):
            add_char = random.choice(char_digits)  # nosec
            self.passwd = self.passwd + add_char
        return self.passwd


class UniqUsernameMixin(object):

    def get_unique_username(self, first_name, last_name):
        self.user_name = first_name + last_name
        '''Usernames cannot be longer than 30 characters'''
        if len(self.user_name) > 29:
            '''get last characters of long name'''
            self.user_name = self.user_name[:29]
        ex_user = User.objects.filter(username=self.user_name)
        if ex_user.exists():
            '''In the unlikely case that the username already exists,
            take last 6 characters of the name and add an underscore
            followed by 5 random characters or digits'''
            name = self.user_name[:-6] + "_"
            char_digits = ascii_letters + digits
            for x in range(0, 4):
                add_char = random.choice(char_digits)  # nosec
                name = name + add_char
            self.user_name = name
            return self.user_name
        else:
            return self.user_name

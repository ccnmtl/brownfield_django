import json
import random
from string import letters, digits
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponseNotAllowed, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


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


class PasswordMixin(object):

    def get_password(self):
        char_digits = letters + digits
        self.passwd = ''
        for x in range(0, 7):
            add_char = random.choice(char_digits)
            self.passwd = self.passwd + add_char
        return self.passwd


class UniqUsernameMixin(object):

    def get_unique_username(self, first_name, last_name):
        create_name = first_name + last_name
        name = create_name
        '''Usernames cannot be longer than 30 characters'''
        if len(name) > 29:
            '''get last characters of long name'''
            name = create_name[:-29]
        ex_user = User.objects.get(username=name)
        if ex_user.exists():
            '''In the unlikely case that the username already exists,
            take last 6 characters of the name and add an underscore
            followed by 5 random characters or digits'''
            name = create_name[:-6] + "_"
            char_digits = letters + digits
            for x in range(0, 4):
                add_char = random.choice(char_digits)
                name = name + add_char
            self.user_name = name
        else:
            self.user_name = name
        return self.user_name

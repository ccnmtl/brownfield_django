from django import forms
from registration.forms import RegistrationForm

from brownfield_django.interactive.models import TEST_OPTIONS


class InteractiveModeForm(RegistrationForm):
    '''This is for the user to select their desired mode,
    don't want to put in the template.'''
    profile_type = forms.ChoiceField(required=True,
                                     choices=TEST_OPTIONS,
                                     default="Visual Reconassence")

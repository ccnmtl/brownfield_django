from django import forms
from django.forms import ModelForm

class InteractiveModeForm(RegistrationForm):
    '''This is for the user to select their desired mode,
    don't want to put in the template.'''
    profile_type = forms.ChoiceField(required=True, choices=INTERACTIVE_TYPE, default="Visual Reconassence")
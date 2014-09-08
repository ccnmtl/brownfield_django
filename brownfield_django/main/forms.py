from django import forms
from django.forms import ModelForm
from registration.forms import RegistrationForm
from registration.signals import user_registered
from brownfield_django.main.models import Course, UserProfile, Team, PROFILE_CHOICES


class CourseForm(ModelForm):
    class Meta:
        model = Course

class TeamForm(ModelForm):
    class Meta:
        model = Team

class StudentForm(ModelForm):
    class Meta:
        model = UserProfile

        
class CreateAccountForm(RegistrationForm):
    '''This is a form class that will be used
    to allow guest users to create guest accounts.'''
    first_name = forms.CharField(
        max_length=25, required=True, label="First Name")
    last_name = forms.CharField(
        max_length=25, required=True, label="Last Name")
    username = forms.CharField(
        max_length=25, required=True, label="Username")
    password1 = forms.CharField(
        max_length=25, widget=forms.PasswordInput, required=True,
        label="Password")
    password2 = forms.CharField(
        max_length=25, widget=forms.PasswordInput, required=True,
        label="Confirm Password")
    email = forms.EmailField()
    # consent = forms.BooleanField(required=True)
    profile_type = forms.ChoiceField(required=True, choices=PROFILE_CHOICES)

    def clean_profile_type(self):
        data = self.cleaned_data['profile_type']
        if data == '-----':
            raise forms.ValidationError(
                "Please indicate whether you are faculty, team, or a student.")

def user_created(sender, user, request, **kwargs):
    form = CreateAccountForm(request.POST)

    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user)
    profile.is_faculty = form.data['profile_type']
    profile.save()

user_registered.connect(user_created)
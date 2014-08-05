from django import forms
from django.forms import ModelForm
from brownfield_django.main.models import Course, UserProfile, Team


class CourseForm(ModelForm):
    class Meta:
        model = Course

class TeamForm(ModelForm):
    class Meta:
        model = Team
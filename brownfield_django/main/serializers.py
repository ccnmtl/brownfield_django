# from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers

from brownfield_django.main.models import Course, Document, UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'url', 'name', 'startingBudget', 'enableNarrative',
                  'message', 'active', 'archive', 'professor')


class AddCourseByNameSerializer(serializers.ModelSerializer):
    '''Allow professor to add a course by name as in original brownfield.'''
    class Meta:
        model = Course
        fields = ('name',)


class CourseNameIDSerializer(serializers.ModelSerializer):
    '''Allow professor to add a course by name as in original brownfield.'''
    class Meta:
        model = Course
        fields = ('name', 'id')


class CompleteCourseSerializer(serializers.ModelSerializer):
    '''Allow professor see, update all aspects of a course.'''
    class Meta:
        model = Course
        fields = ('name', 'password', 'startingBudget', 'enableNarrative',
                  'message', 'active', 'professor')


class UpdateCourseSerializer(serializers.ModelSerializer):
    '''Allow professor see, update all aspects of a course.'''
    class Meta:
        model = Course
        fields = ('name', 'startingBudget', 'enableNarrative',
                  'active')


class CompleteDocumentSerializer(serializers.HyperlinkedModelSerializer):
    '''Return Document set with each documents associated attributes.'''
    class Meta:
        model = Document
        fields = ('id', 'name', 'link', 'visible')


class TeamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserProfileSerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = UserProfile
        fields = ('profile_type', 'course')


class CreateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('signed_contract', 'budget')


class NewTeamSerializer(serializers.Serializer):
    pk = serializers.Field()
    name = serializers.CharField(max_length=255)
    signed_contract = serializers.BooleanField()
    # budget = serializers.IntField(required=False)


class ListUserCoursesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('name')


class ListAllCoursesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'startingBudget', 'enableNarrative', 'message',
                  'active', 'creator')


class CourseTeamSerializer(serializers.ModelSerializer):
    teams = serializers.RelatedField(many=True)

    class Meta:
        model = Course
        fields = ('name', 'course', 'signed_contract')


class CourseUserSerializer(serializers.ModelSerializer):
    students = serializers.RelatedField(many=True)

    class Meta:
        model = Course
        # fields = ('first_name', 'last_name', 'email')


# class UserCoursesSerializer(serializers.HyperlinkedModelSerializer):
#     courses = serializers.PrimaryKeyRelatedField(many=True)
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'courses')


# class StudentsInCourseSerializer(serializers.HyperlinkedModelSerializer):
#     courses = serializers.PrimaryKeyRelatedField(many=True)
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'courses')

# from django.forms import widgets
from django.contrib.auth.models import User  # , Group
from rest_framework import serializers
from brownfield_django.main.models import Course, Document, UserProfile


class AddCourseByNameSerializer(serializers.HyperlinkedModelSerializer):
    '''Allow professor to add a course by name as in original brownfield.'''
    class Meta:
        model = Course
        fields = ('name',)


class CourseNameIDSerializer(serializers.HyperlinkedModelSerializer):
    '''Allow professor to add a course by name as in original brownfield.'''
    class Meta:
        model = Course
        fields = ('name', 'id')


class CompleteCourseSerializer(serializers.HyperlinkedModelSerializer):
    '''Allow professor see, update all aspects of a course.'''
    class Meta:
        model = Course
        fields = ('name', 'password', 'startingBudget', 'enableNarrative',
                  'message', 'active', 'professor')


class UpdateCourseSerializer(serializers.HyperlinkedModelSerializer):
    '''Allow professor see, update all aspects of a course.'''
    class Meta:
        model = Course
        fields = ('name', 'password', 'startingBudget', 'enableNarrative',
                  'message', 'active', 'professor')


class CompleteDocumentSerializer(serializers.HyperlinkedModelSerializer):
    '''Return Document set with each documents associated attributes.'''
    class Meta:
        model = Document
        fields = ('id', 'name', 'link', 'visible')


class UserSerializer(serializers.ModelSerializer):
    '''Get three user fields.'''
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = UserProfile
        fields = ('profile_type', 'course', 'team')


class CreateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('name', 'password1', 'password2')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('name', 'signed_contract', 'budget')


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

#
# class CourseSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Course
#         fields = ('name')


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups')
#
#
# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url', 'name')

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

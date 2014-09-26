# from django.forms import widgets
from django.contrib.auth.models import User  # , Group
from rest_framework import serializers
from brownfield_django.main.models import Course, Team
# Serializers define the API representation


class AddCourseByNameSerializer(serializers.HyperlinkedModelSerializer):
    '''Allow professor to add a course by name as in original brownfield.'''
    class Meta:
        model = Course
        fields = ('name',)


class CompleteCourseSerializer(serializers.HyperlinkedModelSerializer):
    '''Allow professor see, update all aspects of a course.'''
    class Meta:
        model = Course
        fields = ('name', 'password', 'startingBudget', 'enableNarrative',
                  'message', 'active', 'creator')


class CompleteDocumentSerializer(serializers.HyperlinkedModelSerializer):
    '''Allow professor see, update all aspects of a course.'''
    class Meta:
        model = Course
        fields = ('name', 'course', 'link', 'visible')


# class UserCoursesSerializer(serializers.HyperlinkedModelSerializer):
#     courses = serializers.PrimaryKeyRelatedField(many=True)
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'courses')


class StudentsInCourseSerializer(serializers.HyperlinkedModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'courses')


class AddStudentToCourseSerializer(serializers.HyperlinkedModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'course', 'team_entity', 'signed_contract', 'budget')


class ListUserCoursesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('name')


class ListAllCoursesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'startingBudget', 'enableNarrative', 'message',
                  'active', 'creator')


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

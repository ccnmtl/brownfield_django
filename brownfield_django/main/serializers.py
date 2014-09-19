from django.forms import widgets
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from brownfield_django.main.models import Course, Team
# Serializers define the API representation

class CourseByNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('name',)

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'password', 'startingBudget', 'enableNarrative',
                  'message', 'active', 'creator')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'courses')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'course', 'team_entity', 'signed_contract', 'budget')

# class ListCourseSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Course
#         fields = ('name')
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
        

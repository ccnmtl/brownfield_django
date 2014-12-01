# from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers

from brownfield_django.main.models import Course, Document, UserProfile, Team


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'url', 'name', 'startingBudget', 'enableNarrative',
                  'message', 'active', 'archive', 'professor')


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    course = serializers.RelatedField()

    class Meta:
        model = Document
        fields = ('id', 'course', 'url', 'name', 'link', 'visible')


class TeamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'username')


class StudentUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'first_name', 'last_name', 'email')


class StudentMUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = UserProfile
        fields = ('profile_type', 'course')


class CompleteTeamSerializer(serializers.ModelSerializer):
    user = serializers.RelatedField()

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'signed_contract', 'budget', 'team_passwd')


class TeamMemberSerializer(serializers.ModelSerializer):
    course = serializers.RelatedField()
    student = StudentMUserSerializer(many=True)

    class Meta:
        model = Team
        fields = ('signed_contract', 'budget', 'students', 'course')


# class TeamMemberSerializer(serializers.ModelSerializer):
#     team = StudentMUserSerializer(many=True)
# 
#     class Meta:
#         model = Team
#         fields = ('signed_contract', 'budget')
#  
#         
# class TeamUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'username')
        
        
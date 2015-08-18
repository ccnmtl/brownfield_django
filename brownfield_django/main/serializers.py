# from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers

from brownfield_django.main.models import Course, Document, UserProfile, Team


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class CourseSerializer(serializers.ModelSerializer):
    '''When working with serializer override create and update
    to allow partial updates'''

    class Meta:
        model = Course
        fields = ('id', 'name', 'startingBudget', 'archive',
                  'message', 'professor')


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'url', 'name', 'link', 'visible', 'course')


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

    class Meta:
        model = UserProfile
        fields = ('profile_type', 'course')


class TeamMemberSerializer(serializers.ModelSerializer):
#    course = serializers.RelatedField()
    students = StudentMUserSerializer(many=True)

    class Meta:
        model = Team
        fields = ('signed_contract', 'budget', 'students', 'course')


class InstructorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('profile_type', 'archive')

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.profile_type = validated_data.get(
            'profile_type', instance.profile_type)
        instance.archive = validated_data.get('archive', instance.archive)
        instance.save()
        return instance


class InstructorSerializer(serializers.ModelSerializer):
    profile = InstructorProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                  'profile')

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.save()
        return instance

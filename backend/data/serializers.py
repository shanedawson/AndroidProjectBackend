from django.contrib.auth.models import User, Group
from rest_framework import serializers

from data.models import *


# The serializers all transform the models into json


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(many=False)
    # student = serializers.Field(source='student')

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups', 'student')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        # attendance = serializers.PrimaryKeyRelatedField(many=True)
        fields = (
            'first_name', 'last_name', 'email', 'user', 'id',
            'cattendance_set', 'formativecase_set', 'selfassesment_set', 'summativecase_set',
            'tattendance_set'
        )


class SummativeCaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SummativeCase


class TAttendanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TAttendance


class CAttendanceSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.Field(source='owner.username')

    class Meta:
        model = CAttendance
        # fields = ('owner', 'week', 'signature', 'comments')


class SelfAssesmentSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.Field(source='owner.username')

    class Meta:
        model = SelfAssesment
        # fields = ('owner', 'task', 'diag', 'well', 'improve', 'average')
        #def perform_create(self, serializer):
        #   serializer.save(owner=self.request.user)


class SelfAssesmentContSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.Field(source='owner.username')

    class Meta:
        model = SelfAssesmentCont


class FormativeCaseSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.Field(source='owner.username')

    class Meta:
        model = FormativeCase
        #fields = ('owner', 'case', 'question_one_mark', 'question_two_mark', 'comment')

import json
import random
import string
import datetime

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views import generic
from django.contrib.auth.models import User, Group
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions

from data.models import Student, TAttendance, CAttendance, SelfAssesment, FormativeCase, SummativeCase, \
    SelfAssesmentCont, AttendanceKey
from data.serializers import (
    StudentSerializer, TAttendanceSerializer,
    CAttendanceSerializer, FormativeCaseSerializer,
    UserSerializer, GroupSerializer, SelfAssesmentSerializer, SummativeCaseSerializer, SelfAssesmentContSerializer
)

# Each Viewset queries each model and calls the respective serializer. A GET request will
# return the model contents while a POST request allows creation, update and
# deletion. The fields for each model are detailed in models.py. Each viewset is
# called by the mapped URL.


def find_user(request):
    student_dict = {}
    student_entry = []
    qs = Student.objects.all()
    for term in request.GET['query'].split():
        q = qs.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term))
        print(len(q))
    for s in q:
        student_entry.append(StudentSerializer(s).data)

    student_dict['results'] = student_entry
    student_dict['count'] = len(q)
    return JsonResponse(student_dict)


class CheckKey(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        json_data = json.loads(self.request.body.decode(encoding='UTF-8'))
        key = json_data['key']
        print(key)
        if key == AttendanceKey.objects.last().value:
            return JsonResponse({'key': 'valid'})
        else:
            return JsonResponse({'key': 'invalid'})


class GenerateKey(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(self.request.user)
        if self.request.user.is_superuser:
            # now = datetime.datetime.now()
            value = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            k = AttendanceKey()
            k.value = value
            # k.date = str(now)
            k.save()

            return JsonResponse({'key': value})
        else:
            return JsonResponse({'key': 'Unauthorized'})


class IsAdmin(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(self.request.user)
        if self.request.user.is_superuser:
            return JsonResponse({'admin': 'true'})
        else:
            return JsonResponse({'admin': 'false'})


class GetKey(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(self.request.user)
        if self.request.user.is_superuser:
            return JsonResponse({'key': AttendanceKey.objects.last().value})
        else:
            return JsonResponse({'key': 'Unauthorized'})


class TAttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = TAttendanceSerializer

    def get_queryset(self):
        return self.request.user.student.tattendance_set.all()

    def pre_save(self, obj):
        obj.owner = self.request.user.student


class CAttendanceViewSet(viewsets.ModelViewSet):
    queryset = CAttendance.objects.all()
    serializer_class = CAttendanceSerializer

    def get_queryset(self):
        return self.request.user.student.cattendance_set.all()

    def pre_save(self, obj):
        obj.owner = self.request.user.student


class SelfAssesmentViewSet(viewsets.ModelViewSet):
    # queryset = SelfAssesment.objects.all()
    serializer_class = SelfAssesmentSerializer

    def get_queryset(self):
        return self.request.user.student.selfassesment_set.all()

    def pre_save(self, obj):
        obj.owner = self.request.user.student


class SelfAssesmentContViewSet(viewsets.ModelViewSet):
    # queryset = SelfAssesmentCont.objects.all()
    serializer_class = SelfAssesmentContSerializer

    def get_queryset(self):
        return self.request.user.student.selfassesmentcont_set.all()

    def pre_save(self, obj):
        obj.owner = self.request.user.student


class SelfAssesmentStudentList(generics.ListAPIView):
    serializer_class = SelfAssesmentSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return SelfAssesment.objects.filter(owner__id=username)


class CAttendanceStudentList(generics.ListAPIView):
    serializer_class = CAttendanceSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return CAttendance.objects.filter(owner__id=username)


class SelfAssesmentContStudentList(generics.ListAPIView):
    serializer_class = SelfAssesmentContSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return SelfAssesmentCont.objects.filter(owner__id=username)


class TaughtAttendanceStudentList(generics.ListAPIView):
    serializer_class = TAttendanceSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return TAttendance.objects.filter(owner__id=username)


class FormativeCaseViewSet(viewsets.ModelViewSet):
    # queryset = FormativeCase.objects.all()
    serializer_class = FormativeCaseSerializer

    def get_queryset(self):
        return self.request.user.student.formativecase_set.all()

    def pre_save(self, obj):
        obj.owner = self.request.user.student


class SummativeCaseViewSet(viewsets.ModelViewSet):
    # queryset = SummativeCase.objects.all()
    serializer_class = SummativeCaseSerializer

    def get_queryset(self):
        return self.request.user.student.summativecase_set.all()

    def pre_save(self, obj):
        obj.owner = self.request.user.student

        # @detail_route(methods=['post'])
        #def create(self, request, pk):
        #serializer = SummativeCaseSerializer(data=request.data)
        #if serializer.is_valid():
        #serializer['owner'] = Student.objects.filter(id=pk)
        #serializer.save()


class SummativeCaseTeacher(generics.ListCreateAPIView):
    serializer_class = SummativeCaseSerializer

    def pre_save(self, obj):
        username = self.kwargs['username']
        obj.owner = Student.objects.get(id=username)

    def get_queryset(self):
        username = self.kwargs['username']
        return SummativeCase.objects.filter(owner__id=username)


class FormativeCaseTeacher(generics.ListCreateAPIView):
    serializer_class = FormativeCaseSerializer

    def pre_save(self, obj):
        username = self.kwargs['username']
        obj.owner = Student.objects.get(id=username)

    def get_queryset(self):
        username = self.kwargs['username']
        return FormativeCase.objects.filter(owner__id=username)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user


# Below this line is to be replaced
class IndexView(generic.ListView):
    @staticmethod
    def get_queryset():
        return Student.objects.all()


class LoginView(generic.View):
    # Login user or return error
    @staticmethod
    def post(request):
        json_data = json.loads(request.body.decode(encoding='UTF-8'))
        username = json_data['username']
        password = json_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                data = {'success': True}
            else:
                data = {'success': False, 'error': 'Not active user'}
        else:
            data = {'success': False, 'error': 'Wrong login or password'}
        return JsonResponse(data)

    @staticmethod
    def get(request):
        return HttpResponseBadRequest()


class RegisterView(generic.View):
    # Register new user and attach new student object
    @staticmethod
    def post(request):
        try:
            json_data = json.loads(request.body.decode(encoding='UTF-8'))
            first_name = json_data['first_name']
            last_name = json_data['last_name']
            email = json_data['email']
            username = json_data['username']
            password = json_data['password']

            s = Student()
            s.first_name = first_name
            s.last_name = last_name
            s.email = email
            s.user = User.objects.create_user(username, email, password)
            s.user.first_name = s.first_name
            s.user.last_name = s.last_name
            s.user.save()
            s.save()

            return JsonResponse({'register': True})

        except:
            return JsonResponse({'register': False})

    @staticmethod
    def get(request):
        return JsonResponse({'detail': 'Must use POST to register'})


class LogoutView(generic.View):
    # Logout the user
    @staticmethod
    def post(request):
        logout(request)
        return JsonResponse({'logout': True})

    @staticmethod
    def get(request):
        return JsonResponse({'POST': False})

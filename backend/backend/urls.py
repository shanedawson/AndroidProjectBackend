from django.conf.urls import patterns, include, url
from django.contrib import admin
from data import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

# Map each view to a URL suffix.Objects in each set can be accesed through
# appending the id to the url. eg. /students/1
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'tattendance', views.TAttendanceViewSet, base_name='tattendance')
router.register(r'cattendance', views.CAttendanceViewSet, base_name='cattendance')
router.register(r'selfassesment', views.SelfAssesmentViewSet, base_name='selfassesment')
router.register(r'selfassesmentcont', views.SelfAssesmentContViewSet, base_name='selfassesmentcont')
router.register(r'formative', views.FormativeCaseViewSet, base_name='formativecase')
router.register(r'summative', views.SummativeCaseViewSet, base_name='summativecase')
# router.register(r'^register/', views.RegisterView.as_view(), base_name='register')
# router.register(r'^login/', views.LoginView.as_view(), base_name='login')

# Add the paths to our list of URLs mapping to the router paths,django-rest authorization path
# and the admin panel path
urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^api-token-auth/', obtain_auth_token),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^is_admin/', views.IsAdmin.as_view()),
                       url(r'^search/', views.find_user),
                       url(r'^check_key/', views.CheckKey.as_view()),
                       url(r'^get_key/', views.GetKey.as_view()),
                       url(r'^key/', views.GenerateKey.as_view()),
                       url(r'^login/', views.LoginView.as_view()),
                       url(r'^register/', views.RegisterView.as_view()),
                       url(r'^sa/(?P<username>[0-9]+)/$', views.SelfAssesmentStudentList.as_view()),
                       url(r'^ta/(?P<username>[0-9]+)/$', views.TaughtAttendanceStudentList.as_view()),
                       url(r'^ca/(?P<username>[0-9]+)/$', views.CAttendanceStudentList.as_view()),
                       url(r'^ref/(?P<username>[0-9]+)/$', views.SelfAssesmentContStudentList.as_view()),
                       url(r'^sct/(?P<username>[0-9]+)/$', views.SummativeCaseTeacher.as_view()),
                       url(r'^fct/(?P<username>[0-9]+)/$', views.FormativeCaseTeacher.as_view()),
)

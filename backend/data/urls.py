from django.conf.urls import url, patterns

from data import views

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^login/', views.LoginView.as_view(), name='login'),
                       url(r'^register/', views.RegisterView.as_view(), name='register'),
)

from django.contrib.auth import views
from content.views import Login
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name='studyapp'

urlpatterns=[
  path('',views.BeforeLogin,name='BeforeLogin'),
  path('home/',views.print_studytime,name='home'),
  path('login/',Login.as_view(),name='login'),
  path('login/password',views.password,name='password'),
  path('create_user/',views.create_user,name='create_user'),
  path('studylog/',views.studytime,name='studylog'),
  path('registsite/',views.registsite,name='registsite'),
  path('registform',views.registform,name='registform')
]
from django.contrib.auth import views
from content.views import Login
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name='studyapp'

urlpatterns=[
  path('home/',views.home,name='home'),
  path('login/',Login.as_view(),name='login'),
  path('password',views.password,name='password'),
  path('create_user/',views.create_user,name='create_user'),
  path('create_user/',views.createaccount,name='createaccount'),
]
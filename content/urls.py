from django.contrib.auth import logout, views
from content.views import Login, Logout, changepassword,pass_for_changepassword,password_reset_done,CreateNewPassword, timer
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name='studyapp'

urlpatterns=[
  path('',views.BeforeLogin,name='BeforeLogin'),
  path('home/',views.print_studytime,name='home'),
  path('login/',Login.as_view(),name='login'),
  path('logout/',views.Logout,name='logout'),
  path('timer/',views.timer,name='timer'),
  path('password/',views.pass_for_changepassword,name='password'),
  path('password/change/',views.changepassword,name='change_password'),
  path('password/create/',views.CreateNewPassword,name='CreateNewPassword'),
  path('home/password_reset_done/',views.password_reset_done,name='password_reset_done'),
  path('create_user/',views.create_user,name='create_user'),
  path('studylog/',views.studytime,name='studylog'),
  path('registsite/',views.registsite,name='registsite'),
  path('registform',views.registform,name='registform')
]
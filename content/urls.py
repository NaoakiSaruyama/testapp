from django.contrib.auth import logout, views
from content.views import Login, Logout,pass_for_changepassword,password_reset_done,CreateNewPassword, timer#delete
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name='studyapp'

urlpatterns=[
  path('',Login.as_view(),name='login'),
  path('create_user/',views.create_user,name='create_user'),
  path('password/',views.pass_for_changepassword,name='password'),
  path('home/password_reset_done/',views.password_reset_done,name='password_reset_done'),
  path('password/create/',views.CreateNewPassword,name='CreateNewPassword'),
  path('home/',views.print_studytime,name='home'),
  path('logout/',views.Logout,name='logout'),
  path('timer/',views.timer,name='timer'),
  path('studylog/',views.studytime,name='studylog'),
  path('registsite/',views.registsite,name='registsite'),
  path('registsite/delete/<int:delete_id>',views.registsite_delete,name="delete_site"),
  #path('registsite/<str:query>',views.registsite_search,name="registsite_search"),
  path('registform',views.registform,name='registform')
]
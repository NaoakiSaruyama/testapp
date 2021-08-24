from django.contrib.auth import logout, views
from content.views import Login
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
  path('home/search/',views.each_month_studylog_search,name='home_search'),
  path('home/detail/',views.each_total_study_time,name="detail_total"),
  path('home/detail/month/',views.each_month_study_time,name ="detail_month"),
  path('home/detail/day/',views.day_study_time,name="detail_day"),
  path('logout/',views.Logout,name='logout'),
  path('timer/',views.timer,name='timer'),
  path('studylog/',views.studytime,name='studylog'),
  path('studylog/edit',views.edit_studylog,name='edit_studylog'),
  path('studylog/edit/delete/<int:delete_studylog_id>',views.delete_studylog,name='delete_studylog'),
  path('studylog/edit/edit_each_studylog/<int:edit_each_studylog_id>',views.edit_each_studylog,name='edit_each_studylog'),
  path('registsite/',views.registsite,name='registsite'),
  path('registsite/search/',views.registsite_search,name="registsite_search"),
  path('registsite/delete/<int:delete_id>',views.registsite_delete,name="delete_site"),
  path('registsite/edit/<int:edit_id>',views.registsite_edit,name="edit_site"),
  path('registform',views.registform,name='registform'),
]
from content.views import Login
from django.urls import path
from django.urls.resolvers import URLPattern

app_name='studyapp'

urlpatterns=[
  path('home/',home.as_view(),name='home'),
  path('login/',Login.as_view(),name='login'),
]

from content.views import Login
from django.urls import path
from django.urls.resolvers import URLPattern

app_name='studyapp'

urlpatterns=[
  path('login/',Login.as_view(),name='login'),
]
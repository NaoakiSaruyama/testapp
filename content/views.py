from content.forms import LoginForm
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView

class Login(LoginView):
  form_class = LoginForm
  template_name="testapp/content/template/content/SignIn.html"

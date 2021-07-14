from django.http import request
from content.forms import LoginForm
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView

#####ログイン#######
class Login(LoginView):
  form_class = LoginForm
  template_name="content/SignIn.html"
######ログイン終わり#########

#######ホーム(ログイン後)#########
def home(request):
  template_name="content/home-after-login.html"
  return render(request,template_name)
#######ホーム(ログイン後)終わり#######

######アカウント作成#########
def createaccount(request):
  template_name="content/RegistUser.html"
  return render(request,template_name)


#####アカウント作成##########

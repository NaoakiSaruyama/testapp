from django.http import request
from django.views.generic.base import TemplateResponseMixin
from content.forms import LoginForm
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView

#####ログイン#######
class Login(LoginView):
  form_class = LoginForm
  template_name="content/SignIn.html"
######ログイン終わり#########

#######ホーム(ログイン後/リンク)#########
def home(request):
  template_name="content/home-after-login.html"
  return render(request,template_name)
#######ホーム(ログイン後)終わり#######

######アカウント作成(リンク)#########
def create_user(request):
  template_name="content/RegistUser.html"
  return render(request,template_name)


#####アカウント作成##########
def createaccount(request):
  if request.method=='POST':
    object=User.objects.create(
      email=request.POST["Email"],
      name=request.POST["username"],
      password=request.POST["password"],
    )
    object.save()
    return redirect('studyapp:home')
  else:
    return render(request, 'content/RegistUser.html')
#######アカウント作成終了########

#######パスワード再設定(リンク)#########
def password(request):
  template_name="content/ForgetPassword.html"
  return render(request,template_name)
#######パスワード再設定終了############
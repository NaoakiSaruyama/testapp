from django.http import request
from content.forms import LoginForm
from django.shortcuts import redirect, render
from .models import User,StudyTime

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

#####アカウント作成##########
def create_user(request):
  if request.method == 'POST':
    object = User.objects.create(
      email = request.POST['email'],
      name = request.POST['username'],
      password = request.POST['password'],
    )
    object.save()
    return redirect('studyapp:home')
  else:
    return render(request, 'content/RegistUser.html')
#######アカウント作成終了########

#######パスワード再設定1(ユーザー確認)#########
def password(request):
  if request.method=="POST":
    object=User.objects.all
#######パスワード再設定終了############

#####勉強時間の記録#######
def studytime(request):
  if request.mothod=="POST":
    object=StudyTime.objects.all(
      text=request.POST['text'],
      time=request.POST['time'],
      category=request.POST['category'],
    )
    object.save()
    return redirect('studyapp:home')
  else:
    return render(request,'cotent/AddStudyLog.html')

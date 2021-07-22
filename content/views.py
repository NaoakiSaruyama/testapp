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

#####勉強時間の記録#######
def studytime(request):
  if request.method=="POST":
    object=StudyTime.objects.create(
      text=request.POST['text'],
      time=request.POST['time'],
      category=request.POST['category'],
    )
    object.save()
    return redirect('studyapp:home')
  else:
    return render(request,'content/AddStudyLog.html')
#####勉強時間の記録終了#########

#####勉強時間の出力###########
def print_studytime(request):
  object=StudyTime.objects.filter(time,regist_date)
  context={'time':time,'date':regist_date}
  return render(request,'content/home-after-login.html',context)
####勉強時間の出力終了########

####登録サイト(リンク)###########
def registsite(request):
  template_name="content/RegistSite.html"
  return render(request,template_name)
######登録サイト(リンク)終了#######

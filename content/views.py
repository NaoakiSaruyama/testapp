import datetime
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.views import LoginView
from django.conf.urls import url
from django.http.response import HttpResponse
from .models import Userdata,StudyTime,Registsite,UserManager
from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.db.models import Sum
from .forms import EmailAuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.


#####ログイン前#######
def BeforeLogin(request):
  template_name="content/home-before-login.html"
  return render(request,template_name)
#####ログイン前######


#####ログイン#######
class Login(LoginView):
  form_class = EmailAuthenticationForm
  template_name="content/SignIn.html"
######ログイン終わり#########

#####ログアウト#######
def Logout(request):
  logout(request)
  return redirect(request,'studyapp:BeforeLogin')
####ログアウト終了####

#####アカウント作成##########
def create_user(request):
  if request.method == 'POST':
    object = Userdata.objects.create(
      email = request.POST['email'],
      name = request.POST['username'],
      password = request.POST['password'],
    )
    object.save()
    return redirect('studyapp:home')
  else:
    return render(request, 'content/RegistUser.html')
#######アカウント作成終了########

######パスワードの変更(未完成)########

#パスワード変更ページへのリンク
#def pass_for_changepassword(request):
#  return render(request,'content/CreateNewPassword')
def pass_for_changepassword(request):
  if request.method == "POST":
    post_email = request.POST['email']
    associated_users = Userdata.objects.filter(email=post_email)
    if associated_users.exists():
      for user in associated_users:
        subject= "パスワードのリセットを受け付けました"
        email_template_name = "content/password/password_reset_email.txt"
        c={
          "email":user.email,
          'domain':'127.0.0.1:8000',
					'site_name': 'Website',
          "uid":urlsafe_base64_encode(force_bytes(user.pk)),
          "user":user,
          'token':default_token_generator.make_token(user),
          'protocol':'http'
        }
        email = render_to_string(email_template_name,c)
        try:
          send_mail(subject,email,'admin@example.com',[user.email], fail_silently=False)
        except BadHeaderError:
          return HttpResponse('Invalid header found.')
        messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
        return redirect('studyapp:BeforeLogin')
  return render(request,'content/UserCheck.html')

#パスワード変更ページ(要らない)#
def changepassword(request):
  template_name='content/UserCheck.html'
  return render(request,template_name)

########パスワードの変更######

#####勉強時間の記録#######
def studytime(request):
  if request.method=="POST":
    object=StudyTime.objects.create(
      auth=request.user,
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
@login_required
def print_studytime(request):
  total_object=StudyTime.objects.filter(auth=request.user)

  today=datetime.date.today()
  #今日の勉強レコードの登録
  daily_object=total_object.filter(regist_date__date=today)

  # 週の勉強登録レコードを抽出
  week_monday = today - datetime.timedelta(days=today.isoweekday() + 1)
  week_sunday=week_monday+datetime.timedelta(days=6)
  weekly_object=total_object.filter(regist_date__range=[week_monday,week_sunday])

  # 週の合計時間を計算
  weekly_time=weekly_object.aggregate(Sum('time'))
  if weekly_time['time__sum'] is None:
    weekly_time['time__sum']=0

  # 総学習時間
  total_time=total_object.aggregate(Sum('time'))
  if total_time['time__sum'] is None:
    total_time['time__sum']=0

  #今日の学習時間
  daily_time=daily_object.aggregate(Sum('time'))
  if daily_time['time__sum'] is None:
    daily_time['time__sum']=0


  contents={
    'time':total_time['time__sum'], #合計
    'week_time':weekly_time['time__sum'], #今週の合計
    'today_time':daily_time['time__sum'], #今日の合計
    }
  return render(request,'content/home-after-login.html',contents)
####勉強時間の出力終了########

####登録サイト(リンク)###########
def registsite(request):
  template_name="content/RegistSite.html"
  return render(request,template_name)
######登録サイト(リンク)終了#######

#####登録フォーム(未完成)#######
def registform(request):
  if request.method=="POST":
    object=Registsite.objects.create(
      auth=request.user,
      url=request.POST["url"],
      title=request.POST["name"],
      category=request.POST["category"],
    )
    object.save()
    return redirect('studyapp:registsite')
  else:
    return render(request,'content/regist-site-form.html')

def Usersite(request):
  object=Registsite.objects.all(auth=request.user)
  contents={
    'url':object.url,
    'title':object.title,
    'category':object.category,
  }
  return render(request,'content/RegistSite.html',contents)


#####登録フォーム#######

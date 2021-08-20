import datetime
import calendar
from django.contrib import auth
from django.core import paginator
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.views import LoginView
from django.conf.urls import url
from django.http.response import HttpResponse
from .models import Userdata,StudyTime,Registsite
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, logout
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.db.models import Sum, query
from .forms import EmailAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Page, Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

#####ログイン#######
class Login(LoginView):
  form_class = EmailAuthenticationForm
  template_name="content/SignIn.html"
######ログイン終わり#########

#####ログアウト#######
def Logout(request):
  logout(request)
  return redirect(request,'studyapp:login')
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

#パスワード変更用のメール
def pass_for_changepassword(request):
  if request.method == "POST":
    post_email = request.POST['email']
    associated_users = Userdata.objects.filter(email=post_email)
    if associated_users.exists():
      for user in associated_users:
        subject = "パスワードのリセットを受け付けました"
        email_template_name = "content/password/password_reset_email.txt"
        c={
          "email":user.email,
          'domain':'127.0.0.1:8000',
          'site_name': 'Website',
          'username':user.name,
          "uid":urlsafe_base64_encode(force_bytes(user.pk)),
          "user":user,
          'token':default_token_generator.make_token(user),
          'protocol':'http',
        }
        email = render_to_string(email_template_name,c)
        try:
          send_mail(subject,email,'admin@example.com',[user.email], fail_silently=False)
        except BadHeaderError:
          return HttpResponse('Invalid header found.')
        messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
      return redirect('studyapp:password_reset_done')
  return render(request,'content/UserCheck.html')


#パスワード変更後ページ
def password_reset_done(request):
  return render(request,template_name='content/password_reset_done.html')

#パスワード変更ページへのリンク
def CreateNewPassword(request):
  if request.method == 'POST':
    post_email = request.POST['email']
    associated_user =  Userdata.objects.filter(email = post_email)
    if associated_user.exists():
      for user in associated_user:
        user.password = request.POST["password"]
        user.save()
      return redirect('studyapp:home')
  return render(request,'content/CreateNewPassword.html')

########パスワードの変更######

#####勉強時間の記録#######
def studytime(request):
  if request.method=="POST":
    object=StudyTime.objects.create(
      auth=request.user,
      regist_date=request.POST['date'],
      time=request.POST['time'],
      category=request.POST['category'],
    )
    object.save()
    return redirect('studyapp:home')
  else:
    return render(request,'content/AddStudyLog.html')
#####勉強時間の記録終了#########

#####勉強時間の編集(検索前)#####
def edit_studylog(request):
  objects = StudyTime.objects.filter(regist_date__date = datetime.date.today())
  return render(request,'content/EditStudylog.html',{'objects':objects})

####勉強時間の編集(検索後)########
def after_search_edit_studylog(requerst):
  if requerst.method == "GET":
    queryset = StudyTime.objects.filter(auth = requerst.user)
    query = requerst.GET['search']
    if query:
      queryset =  queryset.filter(regist_date_startswhich = query)
    return render(requerst,'content/EditStudylog.html',{'objects':queryset})
  else:
    return redirect('studyapp:edit_studylog')

##削除機能####
@require_POST
def delete_studylog(request,delete_studylog_id):
  studylog = StudyTime.objects.filter(auth = request.user)
  delete_studylog = get_object_or_404(studylog,id = delete_studylog_id)
  delete_studylog.delete()
  return redirect('studyapp:edit_studylog')


###詳細編集機能####
def edit_each_studylog(request,edit_each_studylog_id):
  studylog = StudyTime.objects.filter(auth = request.user)
  edit_studylog = get_object_or_404(studylog,id = edit_each_studylog_id)
  return render(request,'content/EditEachStudylog',{'studylog':edit_studylog})

####編集後再登録####
#def change_studylog(request):
#  if request.method == "POST":


#####勉強時間の出力###########
@login_required
def print_studytime(request):
  total_object=StudyTime.objects.filter(auth=request.user)

  today=datetime.date.today()
  #今日の勉強レコードの抽出
  daily_object = total_object.filter(regist_date__date=today)

  # 週の勉強登録レコードを抽出
  week_monday = today - datetime.timedelta(days=today.isoweekday() + 1)
  week_sunday = week_monday+datetime.timedelta(days=6)
  weekly_object = total_object.filter(regist_date__range=[week_monday,week_sunday])

  # 週の合計時間を計算
  weekly_time = weekly_object.aggregate(Sum('time'))
  #weeklyとtimerweeklyを一時代入してNoneかどうかをチェックする
  if weekly_time['time__sum'] is None:
    weekly_time['time__sum']=0

  # 総学習時間
  total_time = total_object.aggregate(Sum('time'))
  if total_time['time__sum'] is None:
    total_time['time__sum']=0

  #今日の学習時間
  daily_time = daily_object.aggregate(Sum('time'))
  if daily_time['time__sum'] is None:
    daily_time['time__sum']=0


  contents = {
    'time':total_time['time__sum'], #合計
    'week_time':weekly_time['time__sum'], #今週の合計
    'today_time':daily_time['time__sum'], #今日の合計
    }
  return render(request,'content/home-after-login.html',contents)
####勉強時間の出力終了########

###勉強時間(グラフ)###
def each_month_studylog(request):
  if request.method == "GET":
    queryset = StudyTime.objects.filter(auth = request.user)
    query = request.GET['each_month_studylog']
    #datetimeの型にデータを変更
    time =datetime.datetime.strptime(query,'%Y%m')
    #月の初日と次の最終日
    month_first_day=datetime.date(time.year,time.month,1)
    month_end_day = time.replace(day=calendar.monthrange(time.year,time.month)[1])

    day = month_first_day

    days={}
    while day <= month_end_day:
      day +=  datetime.timedelta(days=1)
      days['time']=day

    if query:
      #日付がある場合
      querysets=queryset.filter(regist_date__startswith = query)
      #値がデータベースにないものを抽出(日付すべて(days)-queryの日付(querysets)) →　データベースの再構築
      for day in days:
        some__data = querysets.filter(regist_date__date =  day )
        if some__data is None:
          querysets =querysets.create(
            auth = request.user,
            time = 0,
            regist_date = day,
          )
        else:
          querysets = some__data.aggregate(Sum('time'))
      return render(request,'content/home-after-login.html',{'queryset':querysets})
    else:
      return redirect('studyapp:home')
  return render(request,'content/home-after-login.html')
###勉強時間(グラフ)###


####タイマーの時間記録########
def timer(request):
  if request.method == "POST":
    object = StudyTime.objects.create(
      auth = request.user,
      regist_date = request.POST['date'],
      category = request.POST['category'],
      time = request.POST['time'],
    )
    object.save()
    return redirect('studyapp:timer')
  else:
    return render(request,'content/timer.html')
####タイマーの時間記録終了####


#####登録フォーム#######
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

###登録サイトの出力###
def registsite(request):
  some_object = Registsite.objects.filter(auth=request.user)
  ordered_object = some_object.order_by('-regist_date')
  #ページネーション
  paginator = Paginator(ordered_object,6)
  page = request.Get.get('page',1)
  try:
    pages =paginator.page(page)
  except PageNotAnInteger:
    pages = paginator.page(1)
  except EmptyPage:
    pages = paginator.page(1)

  return render(request,'content/RegistSite.html',{'contents':ordered_object, 'pages': pages})



#削除機能
@require_POST
def registsite_delete(request,delete_id):
  usersites =Registsite.objects.filter(auth=request.user)
  registsite = get_object_or_404(usersites,id=delete_id)
  registsite.delete()
  return redirect('studyapp:registsite')

#編集機能
def registsite_edit(request,edit_id):
  usersites = Registsite.objects.filter(auth=request.user)
  registsite =get_object_or_404(usersites,id=edit_id)
  return render(request,'content/regist_site_edit.html',{'registsite':registsite})

#検索機能
def registsite_search(request):
  if  request.method == "GET":
    auth_site = Registsite.objects.filter(auth=request.user)
    queryset = auth_site.order_by('-regist_date')
    query = request.GET['search']
    if query:
      queryset = queryset.filter(
        Q(title__icontains = query)|Q(category__icontains = query)
    )
    return render(request,'content/RegistSite.html',{'contents':queryset})
  else:
    return render(request,'content/RegistSite.html')
#####登録フォーム#######
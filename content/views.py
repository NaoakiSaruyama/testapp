from django.db.models.query_utils import DeferredAttribute
import content
import datetime
import calendar
import math
import json
from django.contrib import auth
from django.core import paginator
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.views import LoginView
from django.conf.urls import url
from django.db.models.aggregates import Count
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
    return redirect('studyapp:studylog')
  else:
    return render(request,'content/AddStudyLog.html')
#####勉強時間の記録終了#########

#####勉強時間の編集(検索前)#####
def edit_studylog(request):
  objects = StudyTime.objects.filter(regist_date__date = datetime.date.today())
  today = datetime.date.today()
  print(today)
  return render(request,'content/EditStudylog.html',{'objects':objects,'date':str(today)})

####勉強時間の編集(検索後)########
def after_search_edit_studylog(requerst):
  if requerst.method == "GET":
    queryset = StudyTime.objects.filter(auth = requerst.user)
    query = requerst.GET['search']
    if query:
      queryset =  queryset.filter(regist_date__date = query)
    return render(requerst,'content/EditStudylog_after_search.html',{'objects':queryset,'date':query})
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
  regist_date = edit_studylog.regist_date
  date = regist_date.strftime('%Y-%m-%d')

  if request.method == "POST":
    edit_studylog.regist_date =request.POST["date"]
    edit_studylog.category = request.POST["category"]
    edit_studylog.time = request.POST["time"]
    edit_studylog.save()
    return redirect('studyapp:edit_studylog')
  return render(request,'content/EditEachStudylog.html',{'studylog':edit_studylog,'regist_date':date})

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

  #グラフの出力
  user_data = StudyTime.objects.filter(auth = request.user)

  today = datetime.date.today()
  this_month_first_day = today.replace(day = 1)
  this_month_end_day =today.replace(day = calendar.monthrange(today.year,today.month)[1])

  day = this_month_first_day

  days={}

  while day <= this_month_end_day:
    this_month_data = user_data.filter(regist_date__date = day)
    if not len(this_month_data):
      days[f"{day}"] = {"date":day.day,"total":0}
    else:
      days[f"{day}"]={"date":day.day,"total":this_month_data.aggregate(Sum('time'))['time__sum']}

    day +=  datetime.timedelta(days=1)

    date =today.strftime('%Y-%m')


  contents = {
    'time':total_time['time__sum'], #合計
    'week_time':weekly_time['time__sum'], #今週の合計
    'today_time':daily_time['time__sum'], #今日の合計
    'querysets':json.dumps(days),
    'date':date
    }

  return render(request,'content/home-after-login.html',contents)

#検索後
def each_month_studylog_search(request):
  #検索後
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
  #グラフ
  if request.method == "GET":
    queryset = StudyTime.objects.filter(auth = request.user)
    query = request.GET.get('each_month_studylog')
    str_query = str(query)

    if query:
      #datetimeの型にデータを変更
      time =datetime.datetime.strptime(str_query, '%Y-%m')
      #月の初日と次の最終日
      month_first_day=datetime.date(time.year,time.month,1)
      month_end_day = time.replace(day=calendar.monthrange(time.year,time.month)[1]).date()

      day = month_first_day

      days={}
      while day <= month_end_day:
        some__data = queryset.filter(regist_date__date =  day )

        if not len(some__data):
          days[f"{day}"] = {"date":day.day,"total":0}
        else:
          days[f"{day}"] = {"date":day.day,"total":some__data.aggregate(Sum('time'))['time__sum']}

        day +=  datetime.timedelta(days=1)

      contents = {
        'time':total_time['time__sum'], #合計
        'week_time':weekly_time['time__sum'], #今週の合計
        'today_time':daily_time['time__sum'], #今日の合計
        'querysets':json.dumps(days),
        'date':query,
        }

      return render(request,'content/home-after-login.html',contents)
    else:
      return redirect('studyapp:home')

  return render(request,'content/home-after-login.html')
###勉強時間(グラフ)###
####勉強時間の出力終了########

###勉強時間詳細(total)###
def each_total_study_time(request):
  #全体の合計時間
  auth_studytime = StudyTime.objects.filter(auth = request.user)
  total_study_time = auth_studytime.aggregate(Sum('time'))['time__sum']
  print(total_study_time)

  if total_study_time is None:
    total_study_time = 0
    content_sorted=[{
      "category":'記録なし',
      "time":0,
      "width":0,
    }]
    print(total_study_time)

  else:
    categorise =[]

    for item in auth_studytime:
      #分類
      category = item.category
      categorise.append(category)
    categorise = list(set(categorise))


    content=[]

    i = 0
    while i<len(categorise):
      #合計
      category_i = categorise[i]
      each_itme = auth_studytime.filter(category =category_i)
      each_total_study_time = each_itme.aggregate(Sum('time'))['time__sum']
      print(each_total_study_time)
      #データセット作成
      data={
        "category":category_i,
        "time":each_total_study_time,
      }
      content.append(data.copy())

      i += 1
    print(content)

  ##リスト型
    time_lsit = []

    for time in content:
      print(time)
      item = time["time"]
      time_lsit.append(item)
    print(time_lsit)

    max_time = max(time_lsit)
    print(max_time)

    #width
    width = list(map(lambda x:math.floor(x/max_time*100*10**3)/10**3,time_lsit))
    print(width)

    #追加
    j = 0
    for key in content:
      key['width']= width[j]
      j += 1
    print(content)

    #並び替え
    content_sorted = sorted(content,key=lambda x:x['width'], reverse=True)
    print(content_sorted)

  return render(request,'content/studylog_detail_total.html',{'items':content_sorted,'total':total_study_time})

###勉強時間詳細(month)###
def each_month_study_time(request):
  #月の合計時間
  today = datetime.date.today()
  start_month =today.replace(day=1)
  end_month =today.replace(day = calendar.monthrange(today.year,today.month)[1])

  date_ym = today.strftime('%Y-%m')
  print(date_ym)

  auth_studytime = StudyTime.objects.filter(auth = request.user)
  studytime = auth_studytime.filter(regist_date__range = [start_month,end_month])
  month_studytime = studytime.aggregate(Sum('time'))['time__sum']
  print(month_studytime)
  if month_studytime is None:
    month_studytime = 0
    total_width = 0
    content_sorted=[{
      "category":'記録なし',
      "time":0,
      "width":0,
    }]
    print(month_studytime)

  else:
    total_width = 100
    categorise =[]

    for item in studytime:
      #分類
      category = item.category
      categorise.append(category)
    categorise = list(set(categorise))


    content=[]

    i = 0
    while i<len(categorise):
      #合計
      category_i = categorise[i]
      each_itme = studytime.filter(category =category_i)
      each_month_study_time = each_itme.aggregate(Sum('time'))['time__sum']
      print(each_month_study_time)
      #データセット作成
      data={
        "category":category_i,
        "time":each_month_study_time,
      }
      content.append(data.copy())

      i += 1
    print(content)

  ##リスト型
    time_lsit = []

    for time in content:
      print(time)
      item = time["time"]
      time_lsit.append(item)
    print(time_lsit)

    max_time = max(time_lsit)
    print(max_time)

    #width
    width = list(map(lambda x:math.floor(x/max_time*100*10**3)/10**3,time_lsit))
    print(width)

    #追加
    j = 0
    for key in content:
      key['width']= width[j]
      j += 1
    print(content)

    #並び替え
    content_sorted = sorted(content,key=lambda x:x['width'], reverse=True)
    print(content_sorted)

  return render(request,'content/studylog_detail_month.html',{'items':content_sorted,'total':month_studytime,'date':date_ym,'total_width':total_width})

###勉強時間詳細(month検索機能)###
def each_month_study_time_search(request):
  if request.method == "GET":
    #指定付きの合計時間取得
    time = request.GET['search']
    date_ym =datetime.datetime.strptime(str(time) ,'%Y-%m')
    start_month =datetime.date(date_ym.year,date_ym.month,1)
    end_month =date_ym.replace(day = calendar.monthrange(date_ym.year,date_ym.month)[1])

    auth_studytime = StudyTime.objects.filter(auth = request.user)
    studytime = auth_studytime.filter(regist_date__range = [start_month,end_month])
    month_studytime = studytime.aggregate(Sum('time'))['time__sum']
    print(month_studytime)
    if month_studytime is None:
      month_studytime = 0
      total_width = 0
      content_sorted=[{
        "category":'記録なし',
        "time":0,
        "width":0,
      }]
      print(month_studytime)

    else:
      total_width = 100
      categorise =[]

      for item in studytime:
        #分類
        category = item.category
        categorise.append(category)
      categorise = list(set(categorise))


      content=[]

      i = 0
      while i<len(categorise):
        #合計
        category_i = categorise[i]
        each_itme = studytime.filter(category =category_i)
        each_month_study_time = each_itme.aggregate(Sum('time'))['time__sum']
        print(each_month_study_time)
        #データセット作成
        data={
          "category":category_i,
          "time":each_month_study_time,
        }
        content.append(data.copy())

        i += 1
      print(content)

    ##リスト型
      time_lsit = []

      for time in content:
        print(time)
        item = time["time"]
        time_lsit.append(item)
      print(time_lsit)

      max_time = max(time_lsit)
      print(max_time)

      #width
      width = list(map(lambda x:math.floor(x/max_time*100*10**3)/10**3,time_lsit))
      print(width)

      #追加
      j = 0
      for key in content:
        key['width']= width[j]
        j += 1
      print(content)

      #並び替え
      content_sorted = sorted(content,key=lambda x:x['width'], reverse=True)
      print(content_sorted)

  return render(request,'content/studylog_detail_month.html',{'items':content_sorted,'total':month_studytime,'date':time,'total_width':total_width})


###勉強時間詳細(week)###
def each_week_study_time(request):
  #週の合計時間
  today = datetime.date.today()
  week_monday = today - datetime.timedelta(days=today.isoweekday() + 1)
  week_sunday = week_monday+datetime.timedelta(days=6)

  week = today.strftime("%Y-W%W")
  print(week)

  auth_studytime = StudyTime.objects.filter(auth = request.user)
  studytime = auth_studytime.filter(regist_date__range = [week_monday,week_sunday])
  week_studytime = studytime.aggregate(Sum('time'))['time__sum']
  print(week_studytime)
  if week_studytime is None:
    week_studytime = 0
    total_width = 0
    content_sorted=[{
      "category":'記録なし',
      "time":0,
      "width":0,
    }]

  else:
    total_width = 100
    categorise =[]

    for item in studytime:
      #分類
      category = item.category
      categorise.append(category)
    categorise = list(set(categorise))


    content=[]

    i = 0
    while i<len(categorise):
      #合計
      category_i = categorise[i]
      each_itme = studytime.filter(category =category_i)
      each_month_study_time = each_itme.aggregate(Sum('time'))['time__sum']
      print(each_month_study_time)
      #データセット作成
      data={
        "category":category_i,
        "time":each_month_study_time,
      }
      content.append(data.copy())

      i += 1
    print(content)

  ##リスト型
    time_lsit = []

    for time in content:
      print(time)
      item = time["time"]
      time_lsit.append(item)
    print(time_lsit)

    max_time = max(time_lsit)
    print(max_time)

    #width
    width = list(map(lambda x:math.floor(x/max_time*100*10**3)/10**3,time_lsit))
    #追加
    j = 0
    for key in content:
      key['width']= width[j]
      j += 1

    #並び替え
    content_sorted = sorted(content,key=lambda x:x['width'], reverse=True)
    print(content_sorted)

  return render(request,'content/studylog_detail_week.html',{'items':content_sorted,'total':week_studytime,'date':week,'total_width':total_width})

###勉強時間詳細(week検索)###
def each_week_study_time_search(request):
  #週の合計時間
  chosed_week = request.GET["search"]
  week_monday = datetime.datetime.strptime(chosed_week + '-1', "%Y-W%W-%w")
  week_sunday = week_monday+datetime.timedelta(days=6)
  print(week_monday)
  print(week_sunday)

  auth_studytime = StudyTime.objects.filter(auth = request.user)
  studytime = auth_studytime.filter(regist_date__range = [week_monday,week_sunday])
  week_studytime = studytime.aggregate(Sum('time'))['time__sum']
  print(week_studytime)
  if week_studytime is None:
    week_studytime = 0
    total_width = 0
    content_sorted=[{
      "category":'記録なし',
      "time":0,
      "width":0,
    }]

  else:
    total_width = 100
    categorise =[]

    for item in studytime:
      #分類
      category = item.category
      categorise.append(category)
    categorise = list(set(categorise))


    content=[]

    i = 0
    while i<len(categorise):
      #合計
      category_i = categorise[i]
      each_itme = studytime.filter(category =category_i)
      each_month_study_time = each_itme.aggregate(Sum('time'))['time__sum']
      print(each_month_study_time)
      #データセット作成
      data={
        "category":category_i,
        "time":each_month_study_time,
      }
      content.append(data.copy())

      i += 1
    print(content)

  ##リスト型
    time_lsit = []

    for time in content:
      print(time)
      item = time["time"]
      time_lsit.append(item)
    print(time_lsit)

    max_time = max(time_lsit)
    print(max_time)

    #width
    width = list(map(lambda x:math.floor(x/max_time*100*10**3)/10**3,time_lsit))
    #追加
    j = 0
    for key in content:
      key['width']= width[j]
      j += 1

    #並び替え
    content_sorted = sorted(content,key=lambda x:x['width'], reverse=True)
    print(content_sorted)

  return render(request,'content/studylog_detail_week.html',{'items':content_sorted,'total':week_studytime,'date':chosed_week,'total_width':total_width})

###勉強時間詳細(day)###
def day_study_time(request):
  #日の合計時間
  today = datetime.date.today()

  auth_studytime = StudyTime.objects.filter(auth = request.user)#モデルからログインしているユーザーのデータを引っ張る
  studytime = auth_studytime.filter(regist_date__date = today)#今日の日付のデータを抽出する
  today_studytime = studytime.aggregate(Sum('time'))['time__sum']#今日の日付のデータの合計値を出す
  if today_studytime is None:
      today_studytime = 0
      total_width = 0
      content_sorted=[{
        "category":'記録なし',
        "time":0,
        "width":0,
      }]
  else:
    total_width = 100

    categorise =[]

    for item in studytime:
      #分類
      category = item.category
      categorise.append(category)
    categorise = list(set(categorise))


    content=[]

    i = 0
    while i<len(categorise):
      #合計
      category_i = categorise[i]
      each_itme = studytime.filter(category =category_i)
      today_study_time = each_itme.aggregate(Sum('time'))['time__sum']
      print(today_study_time)
      #データセット作成
      data={
        "category":category_i,
        "time":today_study_time,
      }
      content.append(data.copy())

      i += 1

  ##リスト型
    time_lsit = []

    for time in content:
      print(time)
      item = time["time"]
      time_lsit.append(item)
    max_time = max(time_lsit)

    #width
    width = list(map(lambda x:math.floor(x/max_time*100*10**3)/10**3,time_lsit))
    print(width)

    #追加
    j = 0
    for key in content:
      key['width']= width[j]
      j += 1

    #並び替え
    content_sorted = sorted(content,key=lambda x:x['width'], reverse=True)

  return render(request,'content/studylog_detail_day.html',{'items':content_sorted,'total':today_studytime,'date':str(today),'total_width':total_width})

###勉強時間詳細(day検索機能)###
def day_study_time_search(request):
  if request.method == "GET":
    today = request.GET['search']

    auth_studytime = StudyTime.objects.filter(auth = request.user)#モデルからログインしているユーザーのデータを引っ張る
    studytime = auth_studytime.filter(regist_date__date = today)#今日の日付のデータを抽出する
    today_studytime = studytime.aggregate(Sum('time'))['time__sum']#今日の日付のデータの合計値を出す
    if today_studytime is None:
        today_studytime = 0
        total_width = 0
        content_sorted=[{
          "category":'記録なし',
          "time":0,
          "width":0,
        }]
        print(today_studytime)
    else:
      total_width = 100

      categorise =[]

      for item in studytime:
        #分類
        category = item.category
        categorise.append(category)
      categorise = list(set(categorise))


      content=[]

      i = 0
      while i<len(categorise):
        #合計
        category_i = categorise[i]
        each_itme = studytime.filter(category =category_i)
        today_study_time = each_itme.aggregate(Sum('time'))['time__sum']
        print(today_study_time)
        #データセット作成
        data={
          "category":category_i,
          "time":today_study_time,
        }
        content.append(data.copy())

        i += 1
      print(content)

    ##リスト型
      time_lsit = []

      for time in content:
        print(time)
        item = time["time"]
        time_lsit.append(item)
      print(time_lsit)
      max_time = max(time_lsit)
      print(max_time)

      #width
      width = list(map(lambda x:math.floor(x/max_time*100*10**3)/10**3,time_lsit))
      print(width)

      #追加
      j = 0
      for key in content:
        key['width']= width[j]
        j += 1
      print(content)

      #並び替え
      content_sorted = sorted(content,key=lambda x:x['width'], reverse=True)
      print(content_sorted)

  return render(request,'content/studylog_detail_day.html',{'items':content_sorted,'total':today_studytime,'date':today,'total_width':total_width})


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
  pages = some_object.order_by('-regist_date')
  #ページネーション
  paginator = Paginator(pages,6)
  page = request.GET.get('page',1)
  try:
    pages =paginator.page(page)
  except PageNotAnInteger:
    pages = paginator.page(1)
  except EmptyPage:
    pages = paginator.page(1)

  return render(request,'content/RegistSite.html',{'pages': pages})



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

  if request.method == "POST":
    registsite.title = request.POST["name"]
    registsite.category = request.POST["category"]
    registsite.url = request.POST["url"]
    registsite.save()
    return redirect('studyapp:registsite')
  else:
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
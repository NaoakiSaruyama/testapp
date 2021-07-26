from content.views import Login
from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator

# Create your models here.


#ユーザー登録
class User(models.Model):
  name = models.CharField(verbose_name='ユーザー名',max_length=15,unique=True)
  email = models.EmailField(verbose_name='ユーザーid',max_length=30,unique=True)
  password = models.CharField(verbose_name='パスワード',max_length=15)
  regist_date = models.DateTimeField(default=timezone.now)

#学習時間
class StudyTime(models.Model):
  auth=models.ForeignKey(User)
  text=models.CharField(verbose_name='テキスト名',max_length=30)
  time=models.PositiveSmallIntegerField(verbose_name='勉強時間',validators=[MaxLengthValidator(1440)])
  category=models.CharField(verbose_name='分類',max_length=20)
  regist_date=models.DateTimeField(default=timezone.now)

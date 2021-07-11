from django.db import models
from django.utils import timezone
from django.db.models.fields import CharField, DateTimeField

# Create your models here.


#ユーザー登録
class User(models.Model):
  name = models.CharField(verbose_name='ユーザー名',max_length=15)
  id = models.CharField(verbose_name='ユーザーid',max_length=30,primary_key=True)
  password = models.CharField(verbose_name='パスワード',max_length=15)
  regist_date = models.DateTimeField(default=timezone.now)
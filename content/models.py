from typing import Text
from django.conf.urls import url
from django.contrib import auth
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
# Create your models here.

#ユーザー登録
class UserManager(BaseUserManager):
  def create_user(self,username,email,date,password=None):
    if not username:
      raise ValueError('Users must have an name')
    elif not email:
      raise ValueError('Users must have an email adress')
    user = self.model(
      name=username,
      email = self.normalize_email(email),
      regist_date=date,
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self,username,email,password):
    user=self.create_user(
      username,
      email,
      password=password
    )
    user.is_admin =True
    user.save(using=self._db)
    return user

class Userdata(AbstractBaseUser,PermissionsMixin):
  name = models.CharField(verbose_name='ユーザー名',max_length=15,unique=True)
  email = models.EmailField(verbose_name='ユーザーid',max_length=30,unique=True)
  password = models.CharField(verbose_name='パスワード',max_length=15)
  regist_date = models.DateTimeField(default=timezone.now)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)

  objects=UserManager()#Userdata.objectsの時に使うobjects

  EMAIL_FIELD = 'email'# email = models.EmailField(verbose_name='ユーザーid',max_length=30,unique=True)
  USERNAME_FIELD = 'email'# email = models.EmailField(verbose_name='ユーザーid',max_length=30,unique=True)
  REQUIRED_FIELDS = []


#学習時間
class StudyTime(models.Model):
  auth=models.ForeignKey(Userdata,on_delete=models.CASCADE,null=True)
  text=models.CharField(verbose_name='テキスト名',max_length=30)
  time=models.PositiveSmallIntegerField(verbose_name='勉強時間',validators=[MaxLengthValidator(1440)])
  category=models.CharField(verbose_name='分類',max_length=20)
  regist_date=models.DateTimeField(default=timezone.now)

#登録サイト
class Registsite(models.Model):
  auth=models.ForeignKey(Userdata,on_delete=models.CASCADE,null=True)
  url=models.URLField()
  title=models.CharField(verbose_name="サイト名",max_length=30)
  category=models.CharField(verbose_name="分類",max_length=30)
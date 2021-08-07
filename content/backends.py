from django.contrib.auth.backends import ModelBackend
from .models import Userdata

class Userbackend(ModelBackend):
  def authenticate(self,request,email=None,password=None,**kwargs):
    try:
      user=Userdata.objects.get(email=email)
    except Userdata.DoesNotExist:
      return None
    else:

      if password == user.password and self.user_can_authenticate(user):
        return user
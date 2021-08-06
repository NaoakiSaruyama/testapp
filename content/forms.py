from django.contrib.auth.backends import UserModel
from django.contrib.auth import (authenticate, get_user_model)
from django.forms import  Form
from django.forms.fields import EmailField
from django import forms

from django.contrib.auth.forms import (
    AuthenticationForm
)
from django.utils.translation import gettext_lazy as _
from django.utils.text import capfirst

from .models import Userdata



#######ログイン########
class EmailAuthenticationForm(Form):
  email=EmailField(
    label=('Email'),
    widget=forms.EmailInput(attrs={'autofocus':True,})
  )

  password=forms.CharField(
    label=('パスワード'),
    strip=False,
    widget=forms.PasswordInput,
  )

  error_messages = {
        'invalid_login': _(
            "%(username)s とパスワードが一致しません。訂正してください。"
        ),
        'inactive': _("This account is inactive."),
    }

  def __init__(self, request=None, *args, **kwargs):
    self.request = request
    self.user_cache = None
    kwargs.setdefault('label_suffix', '')
    super().__init__(*args,**kwargs)

    self.email_field=UserModel._meta.get_field(UserModel.USERNAME_FIELD)
    self.fields['email'].max_length = self.email_field.max_length or 254
    if self.fields['email'].label is None:
      self.fields['email'].label=capfirst(self.email_field.verbose_name)
    for field in self.fields.values():
      field.widget.attrs["placeholder"]=field.label

  def clean(self):
    email=self.cleaned_data.get('email')
    password=self.cleaned_data.get('password')

    if email is not None and password:
      self.user_cache= authenticate(self.request, email=email, password=password)
      if self.user_cache is None:
        raise self.get_invalid_login_error()
      else:
        self.confirm_login_allowed(self.user_cache)

      return self.cleaned_data


    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )


    def get_user(self):
      return self.user_cache

    def get_invalid_login_error(self):
      return forms.ValidationError(
        self.error_messages['invalid_login'],
        code='invalid_login',
        params={'username':_('Email')},
      )
######ログイン終わり#######




from django.contrib.auth.forms import AuthenticationForm

#######ログイン########
class LoginForm(AuthenticationForm):
  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values:
        field.widget.attrs['placeholder']=field.label
######ログイン終わり#######
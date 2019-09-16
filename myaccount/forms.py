from django import forms
from django.contrib.auth.models import User, AbstractUser

from myaccount.models import Profile


# 회원가입
class UserForm(forms.ModelForm): # signup Form 으로 이용된다.
    class Meta:
        # model = User # Django에서 기본적으로 제공하는 User를 가져와서 사용
        model = Profile # Django에서 기본적으로 제공하는 User를 가져와서 사용
        fields = ['username', 'password', 'password_check']
        widget = {
            'password': forms.PasswordInput(),
            'password_check': forms.PasswordInput(),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('아이디가 이미 사용중입니다.')
        return username


#로그인
class LoginForm(forms.ModelForm): # Login 시 사용된다.
    class Meta:
        model = User
        fields = ['username', 'password'] # 로그인 시에는 username과 password 입력
        widgets = {
            'password': forms.PasswordInput()
            # attrs={'placeholder': 'Enter description here'}),
        }
        help_texts = {
            'username': None,
        }
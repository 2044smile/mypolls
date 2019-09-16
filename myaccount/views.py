from django.http import HttpResponse
from django.shortcuts import render, redirect

from myaccount.forms import LoginForm
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # 가져온 username과 password에 해당하는 User가 있는지 판단
        # 존재할 경우 user변수에는 User인스턴스가 할당되며,
        # 존재하지 않으면 None이 할당된다.
        if user is not None: # username과 password 가 동일하면, Not None이라면
            auth_login(request, user) # 로그인하라
            return redirect('polls:index') # 로그인 후에는 index 페이지를 띄워라
        else:
            return render(request, 'myaccount/login.html', {'form': form, 'error': '아이디와 패스워드를 확인해주세요.'})
    else: # method가 GET인 경우 사용자가 username과 password을 입력할 수 있게 form 제공
        form = LoginForm()
        return render(request, 'myaccount/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('polls:index')


def signup(request):
    if request.method == "POST": # form이 작성된 상태(POST)로 들어온다면
        form = UserForm(request.POST) # UserForm 의 POST 요청을 form 에 저장
        if request.POST['password'] == request.POST['password_check']\
                and len(request.POST['password']) >= 8:
            if form.is_valid(): # UserForm의 입력 된 값들이 유효한지 유효성 검사
                new_user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password']
                ) # 유효성 검사가 완료 된 정상적인 데이터로 유저를 생성
                auth_login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('myaccount:index')
            else:
                return render(request, 'myaccount/signup.html', {'form': form, 'error': '이미 존재하는 아이디입니다.'})
        else:
            if len(request.POST['password']) < 8:
                return render(request, 'myaccount/signup.html', {'form': form, 'error': '패스워드는 8자 이상이여야 합니다.'})
            return render(request, 'myaccount/signup.html', {'form': form, 'error': '패스워드가 일치하지 않습니다.'})
    else:
        form = UserForm()
        return render(request, 'myaccount/signup.html', {'form': form})
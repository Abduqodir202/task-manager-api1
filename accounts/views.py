from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import RegisterForm, LoginForm, ProfileForm, ResetPasswordForm, CodeForm
from accounts.models import VerificationCode, User
from common.service import thread_send_email


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            return redirect('book_list')
        return render(request, 'accounts/login.html', {'form': form})
    form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    if request.method == 'GET':
        form = ProfileForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'form': form})
    else:
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('book_list')
        return render(request, 'accounts/profile.html', {'form': form})


class ForgotPassword(View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'accounts/password_reset_form.html', {'form': form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # to do emailga xat jonatamiz
            user = User.objects.filter(email=email).first()
            if user:
                code = VerificationCode.objects.create(user=user)
                thread_send_email(email, 'parolni tiklash uchun emailga xat', f'code : {code.code}')
            return redirect('password_reset_done')
        return render(request, 'accounts/password_reset_form.html', {'form': form})


class PasswordResetDoneView(View):
    def get(self, request):
        form = CodeForm()
        return render(request, 'accounts/password_code_verificatoin.html', {'form': form})

    def post(self, request):
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            password = form.cleaned_data.get('password')

            user = VerificationCode.objects.filter(code=code).first().user
            if user:
                VerificationCode.objects.filter(user=user).delete()
                user.set_password(password)
                user.save()
                return redirect('login')
            return render(request, 'accounts/password_code_verificatoin.html', {'form': form})
        return render(request, 'accounts/password_code_verificatoin.html', {'form': form})

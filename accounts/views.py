from core import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import RegisterForm, LoginForm, ProfileForm, ResetPasswordForm, CodeForm, TotpForm
from accounts.models import VerificationCode, User
from common.service import thread_send_email
import requests


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


def google_login_page(request):
    url = (f'{settings.GOOGLE_AUTH_URL}'
           f'?client_id={settings.GOOGLE_CLIENT_ID}'
           f'&redirect_uri={settings.GOOGLE_REDIRECT_URI}'
           f'&response_type=code'
           f'&scope=openid email profile')
    return redirect(url)


def google_login_callback(request):
    code = request.GET.get('code')
    token_data = {"code": code,
                  "client_id": settings.GOOGLE_CLIENT_ID,
                  "client_secret": settings.GOOGLE_CLIENT_SECRET,
                  "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                  "grant_type": "authorization_code", }
    token = requests.post(
        settings.GOOGLE_TOKEN_URL, data=token_data
    ).json()

    access_token = token.get('access_token')

    user_info = requests.get(
        settings.GOOGLE_USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"}
    ).json()
    user, _ = User.objects.get_or_create(
        email=user_info.get('email'),
        defaults={
            'first_name': user_info.get('given_name'),
            'last_name': user_info.get('family_name'),
            'username': user_info.get('id'),
        }
    )
    if user.is_2fa_enabled:
        user.generate_totp_secret()
        thread_send_email(user.email, 'totp', f'code : {user.totp_secret}')
        return redirect('verify_totp')
    login(request, user)
    return redirect('book_list')


def verify_totp(request):
    if request.method == 'POST':
        form = TotpForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            user = User.objects.get(totp_secret=code)
            login(request, user)
            return redirect('book_list')
        return render(request, 'accounts/totp.html', {'form': form})
    form = TotpForm()
    return render(request, 'accounts/totp.html', {'form': form})

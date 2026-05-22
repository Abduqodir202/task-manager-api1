from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # path('', include('allauth.urls')),
    path('google_login_page/', views.google_login_page, name='google_login_page'),
    path('google/login/callback/', views.google_login_callback, name='google_login_callback'),
    path('verify_totp/', views.verify_totp, name='verify_totp'),

    path('register/', views.register, name='register'),
    path('login-page/', views.login_view, name='login'),
    path('logout-page/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),

    # django builtin forget password
    # path('forgot-password/',
    #      auth_views.PasswordResetView.as_view(
    #          template_name='registration/password_reset_form.html'
    #      ), name='password_reset'),

    # # 2) "Email yuborildi" xabari
    # path('forgot-password/done/',
    #      auth_views.PasswordResetDoneView.as_view(
    #          template_name='registration/password_reset_done.html'
    #      ), name='password_reset_done'),
    #
    # # 3) Yangi parol kiritish (email'dagi link orqali)
    # path('reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='registration/password_reset_confirm.html'
    #      ), name='password_reset_confirm'),
    #
    # # 4) Muvaffaqiyat sahifasi
    # path('reset/done/',
    #      auth_views.PasswordResetCompleteView.as_view(
    #          template_name='registration/password_reset_complete.html'
    #      ), name='password_reset_complete'),
    path('forgot-password/',
         views.ForgotPassword.as_view(),
         name='password_reset'),

    path('forgot-password/done/',
         views.PasswordResetDoneView.as_view(), name='password_reset_done'),
]

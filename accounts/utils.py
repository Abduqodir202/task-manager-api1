from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from accounts.models import UserRole


def login_required_custom(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:  # sorov.foydalanuvchi
            return func(request, *args, **kwargs)
        else:
            return redirect(settings.LOGIN_URL)

    return inner


def is_poster(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == UserRole.POSTER:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied('Forbidden')

    return inner

def is_moderator(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == UserRole.MODERATOR:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied('Forbidden')

    return inner

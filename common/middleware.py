import datetime

from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils import timezone


class LogIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR', 'Noma\'lum IP')
        now = datetime.datetime.now()
        print(f"[{now}] So'rov IP: {ip}")

        response = self.get_response(request)
        return response


class TimeLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = timezone.now()
        if not (9 <= now.hour <= 18):
            return render(request, 'time_limit.html')
        response = self.get_response(request)
        return response

# [{'192.11.0.1'':["... 12",'...12.1','12.3','...13']}]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_transactions, name='create_transactions'),
]

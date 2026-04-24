from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.files_list, name='files_list'),
    path('create/', views.files_create, name='files_create'),
    path('update/<int:pk>/', views.files_update, name='files_update'),
]

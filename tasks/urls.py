from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogoutAPIView


from .views import (
    PostModelViewSet,
    RegisterAPIView,
    LoginAPIView
)

router = DefaultRouter()
router.register(r'posts', PostModelViewSet, basename='posts')

urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),

    path('api/', include(router.urls)),
]
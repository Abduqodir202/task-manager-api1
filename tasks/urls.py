from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogoutAPIView
from rest_framework.authtoken.views import obtain_auth_token



from .views import (
    PostModelViewSet,
    LoginAPIView
)

router = DefaultRouter()
router.register(r'posts', PostModelViewSet, basename='posts')

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),
    path('api/token/', obtain_auth_token, name='token'),

    path('api/', include(router.urls)),
]
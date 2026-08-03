from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import Post
from .serializers import PostSerializer


# =========================================================
# POST LIST + CREATE
# =========================================================

class PostListCreateAPIView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.select_related("author")
        serializer = PostSerializer(posts, many=True)

        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)

            return Response({
                "success": True,
                "message": "Post yaratildi",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# =========================================================
# POST DETAIL
# =========================================================

class PostDetailAPIView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)

        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "success": True,
                "message": "Post yangilandi",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()

        return Response({
            "success": True,
            "message": "Post o'chirildi"
        }, status=status.HTTP_204_NO_CONTENT)


# =========================================================
# PAGINATION
# =========================================================

class PostPagination(PageNumberPagination):
    page_size = 5


# =========================================================
# POST MODEL VIEWSET
# =========================================================

from django.core.cache import cache

class PostModelViewSet(ModelViewSet):

    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

    throttle_classes = [
        AnonRateThrottle,
        UserRateThrottle,
    ]

    pagination_class = PostPagination

    filterset_fields = {
        "created_at": ["exact", "year", "month", "day"],
        "title": ["exact", "icontains"],
        "content": ["exact", "icontains"],
    }

    search_fields = [
        "title",
        "content",
    ]

    ordering_fields = [
        "created_at",
        "title",
        "id",
    ]

    ordering = [
        "-created_at",
    ]

    # List API ni 60 sekund cache qilish
    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # POST
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        cache.clear()

    # PUT / PATCH
    def perform_update(self, serializer):
        serializer.save()
        cache.clear()

    # DELETE
    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()
# =========================================================
# LOGIN
# =========================================================

class LoginAPIView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)

            return Response({
                "success": True,
                "message": "Login successful",
                "username": user.username
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)


# =========================================================
# LOGOUT
# =========================================================

class LogoutAPIView(APIView):

    def post(self, request):
        logout(request)

        return Response({
            "success": True,
            "message": "Logout successful"
        }, status=status.HTTP_200_OK)


# =========================================================
# CHAT PAGE
# =========================================================

def chat(request):
    return render(request, "chat.html")
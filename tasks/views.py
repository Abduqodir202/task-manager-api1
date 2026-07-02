from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404
from django.contrib.auth import logout, authenticate, login

from .models import Post
from .serializers import PostSerializer



class PostListCreateAPIView(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Post yaratildi",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):

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



class PostPagination(PageNumberPagination):
    page_size = 5



class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

    pagination_class = PostPagination


    # FILTER
    filterset_fields = {
        'created_at': ['exact', 'year', 'month', 'day'],
        'title': ['exact', 'icontains'],
        'content': ['exact', 'icontains'],
    }

    # SEARCH
    search_fields = ['title', 'content']

    # ORDERING
    ordering_fields = ['created_at', 'title', 'id']
    ordering = ['-created_at']


class LoginAPIView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

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



class LogoutAPIView(APIView):

    def post(self, request):
        logout(request)

        return Response({
            "success": True,
            "message": "Logout successful"
        }, status=status.HTTP_200_OK)
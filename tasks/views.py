from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Post
from .serializers import PostSerializer


class PostListCreateAPIView(APIView):

    # GET → barcha data
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    # POST → yangi object
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

    # GET → bitta post
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)

        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    # PUT → update
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

    # DELETE → status
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()

        return Response({
            "success": True,
            "message": "Post o'chirildi"
        }, status=status.HTTP_204_NO_CONTENT)
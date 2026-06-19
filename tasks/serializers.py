from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Title bo'sh bo'lishi mumkin emas."
            )
        return value

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Content kamida 10 ta belgidan iborat bo'lishi kerak."
            )
        return value
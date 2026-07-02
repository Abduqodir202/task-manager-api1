from rest_framework import serializers
from django.contrib.auth.models import User

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
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Content kamida 10 ta belgidan iborat bo'lishi kerak."
            )
        return value

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Parollar mos emas")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])  # 🔥 shart
        user.save()
        return user
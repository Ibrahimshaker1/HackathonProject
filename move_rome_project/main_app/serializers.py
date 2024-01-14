from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("username", "email", "password")
        extra_kwargs = {'password': {'write_only': True}}



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=250)


class UserDataSerialize(serializers.Serializer):
    user_token = serializers.CharField(max_length=250)


class UploadVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UploadedVideo
        fields = ("name", "video_file", "video_image")


class RoomCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)



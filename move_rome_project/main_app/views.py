from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, UserLoginSerializer, UserDataSerialize
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
# Create your views here.


class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLogin(APIView):
    serializer_class = UserLoginSerializer
    def post(self, request, format=None):
        users = User.objects.all()
        username = request.data.get("username")
        password = request.data.get("password")
        print(username)
        print(password)
        user = False
        for my_user in users:
            if my_user.username == username and my_user.password == password:
                user = my_user
        print(user)
        if user:
            login(request, user)
            token, create = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "token": token.key
                }
            )
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class Userdata(APIView):
    serializer_class = UserDataSerialize

    def post(self, request, format=None):
        users = User.objects.all()
        user_input_token = request.data.get("user_token")
        for my_user in users:
            token, create = Token.objects.get_or_create(user=my_user)
            if token.key == user_input_token:
                return Response(
                    {
                        "id": my_user.id,
                        "username": my_user.username,
                        "password": my_user.password,
                        "email": my_user.email,
                        "date_joined": my_user.date_joined
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "rong token key"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )




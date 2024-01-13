from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import User, UploadedVideo
from .serializers import UserSerializer, UserLoginSerializer, UserDataSerialize, UploadVideoSerializer
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser
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


class UploadVideoView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadVideoSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class GetVideos(APIView):
    def get(self, request, format=None):
        try:
            videos = UploadedVideo.objects.all()
            print(videos)
            videos_dic = {}
            number_of_video = 1
            for video in videos:
                videos_dic[str(number_of_video)] = {
                    "id": video.id,
                    "name": video.name,
                    "video_file": video.video_file.url,
                    "video_image": video.video_image,
                    "uploaded_data": video.uploaded_data,
                }
                number_of_video += 1
            print(videos_dic)
            return Response(
                videos_dic,
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {"there is no uploaded videos"},
                status=status.HTTP_200_OK
            )

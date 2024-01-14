from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import User, UploadedVideo, Room
from django.db import models
from .serializers import UserSerializer, UserLoginSerializer, UserDataSerialize, UploadVideoSerializer, RoomCreateSerializer
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
import mimetypes
from django.conf import settings
import os
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
        user = False
        for my_user in users:
            if my_user.username == username and my_user.password == password:
                user = my_user
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
            videos_list = []
            for video in videos:
                videos_list.append({
                    "id": video.id,
                    "name": video.name,
                    "video_file": video.video_file.url,
                    "video_image": video.video_image,
                    "uploaded_data": video.uploaded_data,
                })
            return Response(
                {"videos_dict":videos_list},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {"there is no uploaded videos"},
                status=status.HTTP_200_OK
            )

class RoomCreateView(APIView):
    serializer_class = RoomCreateSerializer
    def post(self, request, pk, second_pk):
        name = request.data.get("name")
        room_video = UploadedVideo.objects.get(pk=pk)
        create_of_room = User.objects.get(pk=second_pk)
        new_room = Room(
            name=name,
            video=room_video,
            creator=create_of_room,
        )
        new_room.save()
        return Response(
            {"message": "room is created"},
            status=status.HTTP_200_OK
        )

class GetRooms(APIView):
    def get(self, request, format=None):
        rooms = Room.objects.all()
        room_list = []
        for room in rooms:
            room_list.append({
                "id": room.id,
                "name": room.name,
                "users_in_room":room.user_in_room,
                "creator":room.creator.username,
                "video_id": room.video.id
            })
        return Response(
            {"rooms_dict": room_list},
            status=status.HTTP_200_OK
        )


class InterRoom(APIView):
    def get(self, request, room_pk, user_id):
        users = User.objects.all()
        user = User.objects.get(pk=user_id)
        room = Room.objects.get(pk=room_pk)
        user.inter_room_id = room.id
        user.save()
        count = 0
        users_in_room_id_list = []
        for my_user in users:
            if my_user.inter_room_id == room_pk:
                count += 1
                users_in_room_id_list.append(my_user.id)
        room.user_in_room = count
        room.save()
        return Response({
            "room_id": room.id,
            "user_in_room_id_list": users_in_room_id_list
        },
            status=status.HTTP_200_OK)


class StreamingView(APIView):
    def get(self, request, room_pk):
        room = Room.objects.get(pk=room_pk)
        video_file = room.video.video_file
        video_path = os.path.join(settings.MEDIA_ROOT, str(video_file))
        chunk_size = 8192
        print(os.path.getsize(video_path))
        def file_iterator(file, chunk_vale):
            with open(file, 'rb') as video:
                while True:
                    chunk = video.read(chunk_vale)
                    if not chunk:
                        print("hello")
                        break
                    yield chunk
                print("while break")

        response = StreamingHttpResponse(file_iterator(video_path, chunk_size),
                                         content_type="video/mp4")
        response['Content-Length'] = os.path.getsize(video_path)
        return response



class LeaveRoom(APIView):
    def get(self, request, user_pk, room_pk):
        user = User.objects.get(pk=user_pk)
        room = Room.objects.get(pk=room_pk)
        room.user_in_room = room.user_in_room - 1
        room.save()
        if user.id == room.creator.id:
            room.delete()
        return Response(
            {"message": "you leave the room"},
            status=status.HTTP_200_OK
        )


from django.urls import path, include
from .views import UserSignupView, UserLogin, Userdata, UploadVideoView, GetVideos, RoomCreateView, GetRooms, InterRoom, StreamingView, LeaveRoom
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("login/", UserLogin.as_view(), name="login"),
    path("getuser/", Userdata.as_view(), name="get_user"),
    path("uploadVideo/", UploadVideoView.as_view(), name="upload_video"),
    path("getVideo/", GetVideos.as_view(), name="getVideo"),
    path("createRoom/<int:pk>/<int:second_pk>", RoomCreateView.as_view(), name="create_room"),
    path("getRoom/", GetRooms.as_view(), name="get_room"),
    path("interRoom/<int:room_pk>/<int:user_id>/", InterRoom.as_view(), name="inter_room"),
    path("streamingView/<int:room_pk>", StreamingView.as_view(), name="streaming_video"),
    path("leaveRoom/<int:user_pk>/<int:room_pk>/", LeaveRoom.as_view(), name="leave_room")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path, include
from .views import UserSignupView, UserLogin, Userdata, UploadVideoView, GetVideos
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("login/", UserLogin.as_view(), name="login"),
    path("getuser/", Userdata.as_view(), name="get_user"),
    path("uploadVideo/", UploadVideoView.as_view(), name="upload_video"),
    path("getVideo/", GetVideos.as_view(), name="getVideo")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

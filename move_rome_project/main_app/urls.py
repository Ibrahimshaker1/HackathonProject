from django.urls import path, include
from .views import UserSignupView, UserLogin, Userdata
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("login/", UserLogin.as_view(), name="login"),
    path("getuser/", Userdata.as_view(), name="get_user")
]

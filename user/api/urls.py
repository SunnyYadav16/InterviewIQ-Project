from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

from user.api.views import (
    MyObtainTokenPairView,
    MyProfileAPIView,
    UserManagementAPIView,
    RegisterAPIView,
    ChangePasswordAPIView,
    ForgotPasswordAPIView,
)

router = DefaultRouter()

router.register("register", RegisterAPIView, basename="register-api")
router.register("my-profile", MyProfileAPIView, basename="my-profile")
router.register("user-management", UserManagementAPIView, basename="user-management")


urlpatterns = [
    path("", include(router.urls)),
    path("login/", MyObtainTokenPairView.as_view(), name="login-api"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh-token-api"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot-password"),
]

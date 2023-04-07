from rest_framework import mixins, permissions, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from common.tasks import send_email_task
from user.api.permissions import GetUpdateOwnProfile
from user.api.serializers import (
    MyProfileSerializer,
    MyTokenObtainPairSerializer,
    RegisterSerializer,
)
from user.models import User


class RegisterAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    http_method_names = ["post"]


class MyObtainTokenPairView(TokenObtainPairView):
    """_summary_

    Args:
        TokenObtainPairView (_type_): _description_
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = MyTokenObtainPairSerializer


class MyProfileAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    It is used for get My profile and update profile details.
    """

    permission_classes = [GetUpdateOwnProfile]
    serializer_class = MyProfileSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "put", "delete"]


class UserManagementAPIView(viewsets.ModelViewSet):
    """
    User Management apis
    """

    permission_classes = [permissions.IsAdminUser]
    serializer_class = MyProfileSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "delete", "put"]


class ChangePasswordAPIView(APIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = User.objects.filter(email=request.user.email).first()
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        if user.check_password(old_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
            else:
                raise APIException("Both passwords do not match")
        else:
            raise APIException("The Old Password entered was incorrect")
        return Response({"message": "Password changed successfully"})


class ForgotPasswordAPIView(APIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = User.objects.filter(email=request.data.get("email")).first()
        if user:
            # to generate a password without any number.
            allowed_chars = (
                "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789$#%^&*"
            )
            random_password = User.objects.make_random_password(
                length=16,
                allowed_chars=allowed_chars,
            )
            user.set_password(random_password)
            user.save()

            # send an email to the user with the temporary password
            send_email_task.delay(
                "emails/user_forget_password_email.html",
                {"temp_password": random_password},
                user,
                "Your password is changed!",
            )

            return Response({"message": f"Your password changed to {random_password}"})
        return Response({"message": "Something went wrong. Please try again."})

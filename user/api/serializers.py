from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from common.tasks import send_email_task
from common.utils import ChoiceField
from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="Email already exists")
        ],
        error_messages={
            "blank": "Email may not be blank",
            "required": "Email is required",
        },
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        error_messages={
            "blank": "Password may not be blank",
            "required": "Password is required",
        },
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        error_messages={
            "blank": "Confirm Password may not be blank",
            "required": "Confirm Password is required",
        },
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data["email"] = validated_data.get("email").lower()
        validated_data.pop("confirm_password")
        instance = super(RegisterSerializer, self).create(validated_data)
        instance.set_password(validated_data.get("password"))
        instance.save()

        # send an email to the user after successful registration
        send_email_task.delay("emails/user_signup_email.html", {}, instance, "Welcome!")

        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """_summary_

    Args:
        TokenObtainPairSerializer (_type_): _description_
    """

    def validate(self, attrs):
        attrs["email"] = attrs["email"].lower()
        # Default response contains - access token and refresh token
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        # Add custom data you want to include in response
        data.update(
            {
                "id": self.user.id,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
            }
        )
        return data


class MyProfileSerializer(serializers.ModelSerializer):
    """
    My profile Serializer
    """

    gender = ChoiceField(choices=User.GENDER_CHOICES)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "profile_pic",
            "profile_banner",
            "dob",
            "gender",
            "address",
            "city",
            "state",
            "country",
            "meta_data",
            "bio",
        )
        read_only_fields = ("email",)

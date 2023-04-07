from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField

from common.models import UserRefBaseModel

from .managers import UserManager


class User(AbstractUser, UserRefBaseModel):
    """
    User Model
    """

    GENDER_CHOICES = (("M", "male"), ("F", "female"), ("O", "other"))

    username = None
    email = models.EmailField(unique=True, blank=False, null=False)
    is_email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, null=True)
    is_phone_verified = models.BooleanField(default=False)
    profile_pic = models.CharField(max_length=255, null=True)
    profile_banner = models.CharField(max_length=255, null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True)
    address = models.CharField(max_length=500, null=True)  # Address Field
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    meta_data = JSONField(blank=True, null=True)
    bio = models.CharField(max_length=255, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
    all_objects = models.Manager()

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"id-{self.id} email-{self.email}"

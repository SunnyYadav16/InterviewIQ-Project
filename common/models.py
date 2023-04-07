from django.db import models


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class UserRefBaseModel(BaseModel):

    created_by = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )
    modified_by = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )
    deleted_by = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

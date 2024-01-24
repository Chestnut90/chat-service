from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # *first_name to name
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    # TODO : url field
    image = models.ImageField(
        upload_to="images/",
    )

    status_message = models.CharField(
        max_length=100,
        blank=True,
    )

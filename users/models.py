from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
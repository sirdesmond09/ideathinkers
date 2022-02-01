from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    phone = models.CharField(max_length=255, unique=True)
    image_url = models.URLField(null=True, blank=True)
    

    def __str__(self):
        return self.username
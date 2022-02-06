import email
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
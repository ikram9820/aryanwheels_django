from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_file_size

class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='user/profile',validators=[validate_file_size])

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
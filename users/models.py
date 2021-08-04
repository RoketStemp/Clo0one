from django.contrib.auth.models import User
from django.db import models


class CustomUser(models.Model):
    """Extended django User model with new fields profile_photo and description"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(verbose_name='User profile photo', upload_to='images')
    description = models.TextField(verbose_name='User info')

    def __str__(self):
        return self.user.username
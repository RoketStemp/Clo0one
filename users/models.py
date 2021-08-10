from django.contrib.auth.models import User
from django.db import models


class UserSubscribers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class UserSubscriptions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CustomUser(models.Model):
    """Extended django User model with new fields profile_photo and description"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(verbose_name='User profile photo', upload_to='images', blank=True)
    description = models.TextField(verbose_name='User info', blank=True)
    subscribers = models.ManyToManyField(UserSubscribers, blank=True)
    subscriptions = models.ManyToManyField(UserSubscriptions, blank=True)

    def __str__(self):
        return self.user.username

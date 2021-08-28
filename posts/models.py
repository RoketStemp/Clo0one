from django.db import models

from users.models import User


class Posts(models.Model):
    text = models.TextField(verbose_name='Post text', max_length=500)
    post_image = models.ImageField(verbose_name='Post image', upload_to='images', blank=True)
    created_at = models.DateTimeField(verbose_name='Post creating time', auto_now_add=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Post author')

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = 'Posts'


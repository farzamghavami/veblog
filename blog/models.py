from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=30, unique=True)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)


    def __str__(self):
        return self.username


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Comment(models.Model):
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post  = models.ForeignKey(Blog, on_delete=models.CASCADE,)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

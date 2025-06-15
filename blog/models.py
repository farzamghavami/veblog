from django.db import models
from django.contrib.auth.models import AbstractUser

class Time(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        abstract = True


class User(AbstractUser,Time):
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=15, unique=True)


    def __str__(self):
        return self.email


class Blog(Time):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Comment(Time):
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post  = models.ForeignKey(Blog, on_delete=models.CASCADE,)
    content = models.TextField()




from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateField()
    categories = models.ManyToManyField(
        to=Category,
        related_name='categories',
        blank = False,
    )
    def __str__(self):
        return self.title


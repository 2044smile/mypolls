from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    password_check = models.CharField(max_length=100)
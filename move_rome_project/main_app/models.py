from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
import datetime
# Create your models here.


class User(User, PermissionsMixin):
    date_joined = datetime.datetime.now()

    def __str__(self):
        return self.username


class Video(models.Model):
    name = models.CharField(max_length=250)


from django.db import models
from django.contrib.auth.models import AbstractUser



class myUsers(AbstractUser):
    AbstractUser._meta.get_field('email')._unique=True
    nationnality = models.CharField(max_length=200)

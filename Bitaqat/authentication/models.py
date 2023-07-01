from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser


class myUsers(AbstractUser):
    AbstractUser._meta.get_field('email')._unique = True
    AbstractUser._meta.get_field('username')._unique = True

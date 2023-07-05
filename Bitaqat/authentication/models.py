from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


class myUsers(AbstractUser):
    AbstractUser._meta.get_field('email')._unique = True
    AbstractUser._meta.get_field('email').validators = [EmailValidator()]
    AbstractUser._meta.get_field('username')._unique = True

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


class myUsers(AbstractUser):
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=50,unique=True,primary_key=True)

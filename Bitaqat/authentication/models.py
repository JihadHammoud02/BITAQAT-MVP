from django.db import models
from django.contrib.auth.models import AbstractUser


class myUsers(AbstractUser):
    AbstractUser._meta.get_field('email')._unique = True
    last_login = None
    first_name = None
    last_name = None
    date_joined = None

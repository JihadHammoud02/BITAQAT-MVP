from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import myUsers
# Register your models here.


admin.site.register(myUsers,UserAdmin)
from django.urls import path
from LoginAuth import views








app_name = 'LoginAuth'
urlpatterns = [
    path('', views.LoginUsers, name="LoginUsers")
]

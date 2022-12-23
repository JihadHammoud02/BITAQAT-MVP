"""VespiriMVP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from EventOrganizer import views
# A way to namespace your urls.
app_name = 'EventOrganizer'
urlpatterns = [
    path('homepage/', views.Get_homepage, name="Get_homepage"),
    path('create/', views.Create_and_List_events, name="Create_and_List_events"),
    path('profile/', views.Get_profile_page, name="Get_profile_page")
]

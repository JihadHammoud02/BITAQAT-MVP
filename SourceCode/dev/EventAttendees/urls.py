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
from django.conf import settings
from django.conf.urls.static import static
from EventAttendees import views
app_name = 'EventAttendees'
urlpatterns = [
    path('', views.Get_homepage, name="Get_homepage"),
    path('profile/', views.Get_profile_page, name="Get_profile_page"),
     path('Marketplace/', views.Get_Marketplace_Page, name="Get_Marketplace_Page"),
      path('event/<str:event_id>/', views.Get_specific_event_page, name="Get_specific_event_page"),
      path('mintingt/<str:event_id>/',views.mint_nft,name='mint_nft')

]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
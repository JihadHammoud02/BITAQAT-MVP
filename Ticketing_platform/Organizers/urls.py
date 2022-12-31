from django.urls import path, include
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from Guests import views as viewsguest
app_name = 'Organizers'
urlpatterns = [
    path('homepage/', views.renderHomepage, name="renderHomepage"),
    path('profile/',views.renderProfile,name='renderProfile'),
    path('create/',views.createEvents,name='createEvents'),
    path('Marketplace/',views.renderMarketplace,name='renderMarketplace'),
    path('logout/',views.logoutUser,name='logoutUser'),
    path('myEvents/',views.myEvents,name='myEvents'),
    path('Dashboard/<str:eventId>/',views.eventDashboard,name='eventDashboard')

    
]

from django.urls import path, include
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from Fan import views as viewsguest
app_name = 'Club'
urlpatterns = [
    path('homepage/', views.renderHomepage, name="renderHomepage"),
    path('profile/',views.renderProfile,name='renderProfile'),
    path('create/',views.createEvents,name='createEvents'),
    path('Marketplace/',views.renderMarketplace,name='renderMarketplace'),
    path('logout/',views.logoutUser,name='logoutUser'),
    path('myEvents/',views.renderAnalytics,name='myEvents'),
    path('MyGame/<str:eventId>/',views.eventDashboard,name='eventDashboard'),
    path('userData/<str:guestID>/<str:guestName>/',views.renderAttandedEvents,name='renderAttandedEvents'),
    path('checkIn/<str:mintedID_DB>/',views.checkInGuest,name='checkInGuest'),
    path('MyClub/',views.getClubData,name='MyClub'),
    path('getTokenOwners/<str:TokenId>/',views.getTokenOwners,name='getTokenOwners'),
    path('scan-qr-code/', views.qr_ccode_scan_view, name='scan-qr-code'),
    path('check-qr-code/', views.check_qr_code, name='check-qr-code'),

    
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
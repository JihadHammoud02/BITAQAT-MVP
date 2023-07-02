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
    path('create/',  views.createEvents, name='createEvents'),
    path('Marketplace/',  views.renderMarketplace, name='renderMarketplace'),
    path('logout/',  views.logoutUser, name='logoutUser'),
    path('myEvents/',  views.renderAnalytics, name='myEvents'),
    path('MyGame/<str:eventId>/',  views.eventDashboard, name='eventDashboard'),
    path('userData/<str:guestID>/<str:guestName>/',
         views.renderAttendedEvents, name='renderAttendedEvents'),
    path('getTokenOwners/<str:tokenId>/',
         views.getTokenOwners, name='getTokenOwners'),
    path('scan-qr-code/',  views.qrCodeScanView, name='qrCodeScanView'),
    path('check-qr-code/',  views.checkQRCode, name='checkQRCode'),
    path('calculateRoyalty/<int:userId>/',
         views.calculateRoyalty, name='calculateRoyalty'),
    path('calculateVolumeTraded/<int:userId>/',
         views.calculateVolumeTraded, name='calculateVolumeTraded'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

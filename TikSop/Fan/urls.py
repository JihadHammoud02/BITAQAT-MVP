from django.urls import path
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
app_name = 'Fan'

urlpatterns = [
    path('homepage/', views.renderHomepage, name="renderHomepage"),
     path('Marketplace/', views.renderMarketplace, name="renderMarketplace"),
      path('event/<str:event_id>/', views.renderSpecificEventPage, name="renderSpecificEventPage"),
      path('Buy/<str:event_id>/',views.buyTicket,name='buyTicket'),
      path('Myinventory/',views.renderInventory,name='renderInventory'),
      path("img/",views.ReturnImg,name="returnImg")

]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
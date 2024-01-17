from django.urls import path
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
app_name = 'Fan'

urlpatterns = [
    path('homepage/', views.renderHomepage, name="renderHomepage"),
    path('Marketplace/', views.renderMarketplace, name="renderMarketplace"),
    path('Buy/<str:event_id>/', views.buyTicket, name='buyTicket'),
    path('Myinventory/', views.renderInventory, name='renderInventory'),
    path("Mykeys/", views.renderKeys, name="Mykeys"),
    path("verification/<str:token_id>/", views.generate_qr_code, name="verf"),
    path("feedback/",views.giveFeedback,name="feedback"),
     path("receive/", views.ReceiverContractEvents, name="receive")
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

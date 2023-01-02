from django.urls import path
from .views import loginUsers,createAccounts,landingPage
app_name = 'authentication'

urlpatterns = [
    path('', landingPage, name="landingPage"),
    path('login/', loginUsers, name="loginUsers"),
    path('register/',createAccounts,name='createAccounts'),

]

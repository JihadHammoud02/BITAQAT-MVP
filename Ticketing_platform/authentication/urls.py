from django.urls import path
from .views import loginUsers,createAccounts
app_name = 'authentication'

urlpatterns = [

    path('', loginUsers, name="loginUsers"),
    path('register/',createAccounts,name='createAccounts'),

]

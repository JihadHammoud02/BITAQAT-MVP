from django.urls import path
from .views import loginmyUsers,createAccounts,landingPage
app_name = 'authentication'

urlpatterns = [
    path('', landingPage, name="landingPage"),
    path('login/', loginmyUsers, name="loginmyUsers"),
    path('register/',createAccounts,name='createAccounts'),

]

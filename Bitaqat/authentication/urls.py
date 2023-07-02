from django.urls import path, include
from .views import landing_page, login_my_users, create_accounts
app_name = 'authentication'

urlpatterns = [
    path('', landing_page, name="landingPage"),
    path('login/', login_my_users, name="loginmyUsers"),
    path('register/', create_accounts, name='createAccounts'),
    path("debug/", include("debug_toolbar.urls")),

]

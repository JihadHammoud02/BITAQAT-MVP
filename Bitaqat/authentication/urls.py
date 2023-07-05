from django.urls import path, include
from .views import landing_page, login_my_users, create_accounts, password_reset_complete
from django.contrib.auth import views as auth_views
app_name = 'authentication'

urlpatterns = [
    path('', landing_page, name="landingPage"),
    path('login/', login_my_users, name="loginmyUsers"),
    path('register/', create_accounts, name='createAccounts'),
    path("debug/", include("debug_toolbar.urls")),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='authentication/resetpassword.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='authentication/emailsentmsg.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='authentication/resetform.html'), name='password_reset_confirm'),
    path('reset/done/',
         password_reset_complete, name='password_reset_complete')
]

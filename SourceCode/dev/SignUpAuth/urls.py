from django.urls import path
from SignUpAuth import views
app_name = 'SignupAuth'
urlpatterns = [
    path('', views.Create_Accounts, name="Create_Accounts")
]

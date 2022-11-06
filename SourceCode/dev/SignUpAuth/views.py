from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from SignUpAuth.models import Organizers
from SignUpAuth.models import Attandee
# Create your views here.


def Create_Account(request):

    try:
        if request.method == "POST":
            email_client = request.POST.get('emailadd')
            username_client = request.POST.get('username')
            password_client = request.POST.get('pswrd')
            nationnality_client = request.POST.get('nat')
            city_client = request.POST.get('city')
            account_type = request.POST.get('res')
            company_name_client = request.POST.get('organisation')
            user = User.objects.create_user(
                username=username_client, email=email_client, password=password_client)
            user.save()
            if account_type == "Event Organizer":
                account = Organizers(
                    user.pk, nationnality_client, city_client, company_name_client)
                account.save()
            else:
                if account_type == "Event Attandee":
                    account = Attandee(
                        user.pk, nationnality_client, city_client)
                account.save()

            return render(request, "LoginAuth\LoginForm.html")
        else:
            return render(request, "SignUpAuth\SignUpForm.html")
    except IntegrityError as e:
        error_msg = ''
        if str(e) == "UNIQUE constraint failed: auth_user.email":
            error_msg = "An Account with this email address already exists"
            return render(request, "SignUpAuth\SignUpForm.html", {"error_msg_email": error_msg})

        else:
            error_msg = "An Account with this username already exists"
            return render(request, "SignUpAuth\SignUpForm.html", {"error_msg_username": error_msg})


# import email
# from django.shortcuts import render
# from django.contrib.auth.models import User
# from re import template

# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import get_object_or_404, redirect, render
# from django.template import RequestContext, loader
# from django.urls import reverse
# from django.contrib.auth import login,authenticate
# import loginpage
# from django.contrib import messages

# # Create your views here.

# def create_user(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         email_client=request.POST.get('email')
#         password=request.POST.get('pswd')
#         conf_pass=request.POST.get('confirm')
#         all_users=User.objects.all()
#         list_of_emails=[]
#         for mail in all_users:
#             list_of_emails.append(mail.email)
#         if email_client in list_of_emails:
#             return render(request,'loginpage/login.html',{'l4':['error']})

#         user = User.objects.create_user(username,email_client,password)
#         user.first_name=request.POST.get('firstname')
#         user.last_name=request.POST.get('familyname')
#         user.save()
#         return HttpResponseRedirect(reverse('loginpage:check_user'))
#     else:
#         return render(request,'signup/signupform.html')

from django.shortcuts import render, reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from eth_account import Account
import secrets
from Fan.SmartContract import sendFromMother

from Club.models import myClub as Club
from .models import myUsers
from Fan.models import myFan


def create_wallet():
    """
    Create a real crypto wallet.

    :return: The private key and the address of the account.
    """
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return private_key, acct.address


def login_my_users(request):
    """
    Log in the user if the request method is POST and the user is authenticated.

    :param request: The request object containing metadata about the current request.
    :return: The result of the render function.
    """
    if request.method == "POST":
        username_client = request.POST.get('username')
        password_client = request.POST.get('pswrd')
        user = authenticate(request, username=username_client,
                            password=password_client)

        if user is not None:
            user_pk = user.pk
            club_model_check = Club.objects.filter(pk=user_pk).exists()
            fan_model_check = myFan.objects.filter(pk=user_pk).exists()

            if club_model_check:
                login(request, user)
                return HttpResponseRedirect(reverse("Club:renderHomepage"))
            elif fan_model_check:
                login(request, user)
                return HttpResponseRedirect(reverse("Fan:renderHomepage"))

        return render(request, 'authentication/Login.html', {'error_msg': True})
    else:
        return render(request, 'authentication/Login.html')


def create_accounts(request):
    """
    Create a user account and save it in the database.

    :param request: The request object containing metadata about the request.
    :return: The render function.
    """
    try:
        if request.method == "POST":

            email_client = request.POST.get('emailadd')
            username_client = request.POST.get('username')
            password_client = request.POST.get('pswrd')
            password_client_hashed = make_password(password_client)

            try:
                validate_email(email_client)
                print(validate_email(email_client))
            except ValidationError:
                error_msg = "Invalid email address"
                return render(request, "authentication/Registration.html", {"error_msg_valid": error_msg})

            user = myUsers.objects.create(
                username=username_client, email=email_client, password=password_client_hashed)
            user.save()

            wallet = create_wallet()
            public_address = wallet[1]
            private_address = wallet[0]
            account = myFan(user=user, public_key=public_address,
                            private_key=private_address)
            account.save()
            sendFromMother(public_address, 0.2)

            return render(request, "authentication/Login.html")
        else:
            return render(request, "authentication/Registration.html")
    except IntegrityError as e:
        error_msg = ''
        if str(e) == "UNIQUE constraint failed: auth_user.email":
            error_msg = "An account with this email address already exists"
            return render(request, "authentication/Registration.html", {"error_msg_email": error_msg})
        else:
            error_msg = "An account with this username already exists"
            return render(request, "authentication/Registration.html", {"error_msg_username": error_msg})


def landing_page(request):
    return render(request, 'authentication/landingPage.html')


def password_reset_complete(request):
    return render(request, 'authentication/resetdone.html')

from django.shortcuts import render, reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from eth_account import Account
import secrets
from Fan.SmartContract import sendFromMother, AddAuthorizer
from Club.models import myClub as Club
from .models import myUsers
from Fan.models import myFan
import environ
env = environ.Env()
environ.Env.read_env()

def create_wallet():
    """
    Create a cryptocurrency wallet.

    :return: A private key and its corresponding address.
    """
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return private_key, acct.address

def login_my_users(request):
    """
    Log in the user if the request method is POST and the user is authenticated.

    :param request: The HTTP request object.
    :return: HTTP response.
    """
    if request.method == "POST":
        username_client = request.POST.get('username')
        password_client = request.POST.get('pswrd')
        user = authenticate(request, username=username_client, password=password_client)

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

    :param request: The HTTP request object.
    :return: HTTP response.
    """
    try:
        if request.method == "POST":
            email_client = request.POST.get('emailadd')
            username_client = request.POST.get('username')
            password_client = request.POST.get('pswrd')
            password_client_hashed = make_password(password_client)

            try:
                validate_email(email_client)
            except ValidationError:
                error_msg = "Invalid email address"
                return render(request, "authentication/Registration.html", {"error_msg_valid": error_msg})


            # Create two wallets for each user: one for NFTs and one for gas fees
            wallet = create_wallet()  # NFT wallet
            authWallet = create_wallet()  # Auth Wallet

            public_address = wallet[1]
            private_address = wallet[0]

            user = myUsers.objects.create(
                username=username_client, email=email_client, password=password_client_hashed)
            
            account = myFan(user=user, public_key=public_address,
                            private_key=private_address, AuthWallet_public_key=authWallet[1], AuthWallet_private_key=authWallet[0])

            sendFromMother(authWallet[1],0.005)


            user.save()
            account.save()

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
    """
    Render the landing page.

    :param request: The HTTP request object.
    :return: HTTP response.
    """
    return render(request, 'authentication/landingPage.html')

def password_reset_complete(request):
    """
    Render the password reset completion page.

    :param request: The HTTP request object.
    :return: HTTP response.
    """
    return render(request, 'authentication/resetdone.html')

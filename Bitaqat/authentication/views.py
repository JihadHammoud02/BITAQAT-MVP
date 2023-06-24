from django.shortcuts import render
from Club.models import myClub as Club, MintedTickets
from Fan.models import myFan as guest
from django.db import IntegrityError
from .models import myUsers
from eth_account import Account
import secrets
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from Club.query import queryEvents


def createWallet():
    """
    It creates a real crypto wallet
    :return: The private key and the address of the account.
    """
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)

    return (private_key, acct.address)


def loginmyUsers(request):
    """
    If the request method is POST, then get the username and password from the request, 
    authenticate the user, and if the user is authenticated, then redirect to the appropriate page.

    :param request: The request object is a Django object that contains metadata about the current
    request
    :return: the result of the render function.
    """
    if request.method == "POST":
        username_client = request.POST.get('username')
        password_client = request.POST.get('pswrd')
        user = authenticate(request, username=username_client,
                            password=password_client)
        if user is not None:
            Upk = user.pk
            clubModelCheck = Club.objects.filter(pk=Upk).exists()
            if clubModelCheck:
                login(request, user)
                return HttpResponseRedirect(
                    reverse("Club:renderHomepage"))

            else:
                login(request, user)
                return HttpResponseRedirect(
                    reverse("Fan:renderHomepage"))

        else:
            return render(request, 'authentication\Login.html', {'error_msg': True})
    else:
        return render(request, 'authentication\Login.html')


def createAccounts(request):
    """
    It creates a user account and saves it in the database.

    :param request: The request object is an HttpRequest object. It contains metadata about the request,
    including the HTTP method
    :return: the render function.
    """
    try:
        if request.method == "POST":
            email_client = request.POST.get('emailadd')
            username_client = request.POST.get('username')
            password_client = request.POST.get('pswrd')
            password_client_hashed = make_password(password_client)
            user = myUsers.objects.create(
                username=username_client, email=email_client, password=password_client_hashed)
            user.save()
            wallet = createWallet()
            public_addresse = wallet[1]
            private_addresse = wallet[0]
            print(public_addresse)
            print(private_addresse)
            account = guest(user=user, public_crypto_address=public_addresse,
                            private_crypto_address=private_addresse)
            print()
            account.save()

            return render(request, "authentication\Login.html")
        else:
            return render(request, "authentication\Registration.html")
    except IntegrityError as e:
        error_msg = ''
        print(e)
        if str(e) == "UNIQUE constraint failed: auth_user.email":
            error_msg = "An Account with this email address already exists"
            return render(request, "authentication\Registration.html", {"error_msg_email": error_msg})

        else:
            error_msg = "An Account with this username already exists"
            return render(request, "authentication\Registration.html", {"error_msg_username": error_msg})


def landingPage(request):
    return render(request, 'authentication\landingPage.html')

from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import IntegrityError
from SignUpAuth.models import Organizers
from SignUpAuth.models import Attandees
from eth_account import Account
import secrets


def create_wallet():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    
    return(private_key, acct.address)

def Create_Accounts(request):
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
                    account = Attandees(
                        user.pk, nationnality_client, city=city_client,public_crypto_address=create_wallet()[1],private_crypto_address=create_wallet()[0])
                account.save()

            return render(request, "LoginAuth\Login.html")
        else:
            return render(request, "SignUpAuth\Registration.html")
    except IntegrityError as e:
        error_msg = ''
        if str(e) == "UNIQUE constraint failed: auth_user.email":
            error_msg = "An Account with this email address already exists"
            return render(request, "SignUpAuth\Registration.html", {"error_msg_email": error_msg})

        else:
            error_msg = "An Account with this username already exists"
            return render(request, "SignUpAuth\Registration.html", {"error_msg_username": error_msg})



from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from SignUpAuth.models import Organizers
from SignUpAuth.models import Attandee
from django.urls import reverse
# Create your views here.


def check_organizers_db(key):
    all_organizers = Organizers.objects.all()
    found = False
    for user in all_organizers:
        if user.pk == key:
            found = True
            break
    return found


def check_attandee_db(key):
    all_attandee = Attandee.objects.all()
    found = False
    for user in all_attandee:
        if user.pk == key:
            found = True
            break
    return found


def Check_User_account(request):
    if request.method == "POST":
        username_client = request.POST.get('username')
        password_client = request.POST.get('pswrd')
        account_type = request.POST.get('res')
        user = authenticate(request, username=username_client,
                            password=password_client)
        if user is not None:
            if account_type == "Event Organizer":
                if check_organizers_db(user.pk):
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse("EventOrganizer:get_homepage"))

                else:
                    return render(request, 'LoginAuth\LoginForm.html', {'error_msg2': True})
            else:
                if account_type == "Event Attandee":
                    if check_attandee_db(user.pk):
                        login(request, user)
                        return HttpResponseRedirect(
                            reverse("EventOrganizer:get_homepage"))
                    else:
                        return render(request, 'LoginAuth\LoginForm.html', {'error_msg3': True})
                else:
                    return render(request, 'LoginAuth\LoginForm.html', {'error_msg4': True})

        else:
            return render(request, 'LoginAuth\LoginForm.html', {'error_msg': True})
    else:
        return render(request, 'LoginAuth\LoginForm.html')

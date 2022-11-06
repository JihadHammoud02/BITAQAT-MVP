from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/login/  ')
# """
# It renders the homepage.html template and passes the username of the logged in user to the template
# :param request: The request object is the first parameter to every view function. It contains
# information about the request that was made to the server, such as the HTTP method, the path, the
# headers, and the body
# :return: The request, the template, and the user's username.
# """
def get_homepage(request):
    return render(request, 'EventOrganizer\homepage.html', {"user_name": request.user.username})


def get_create_event(request):
    return render(request, 'EventOrganizer\eventcreation.html')

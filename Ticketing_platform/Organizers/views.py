from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import myUsers
from .models import myOrganizers,EventsCreated




# A decorator that checks if the user is logged in. If not, it redirects to the login page.
@login_required(login_url='/login/  ')
def renderHomepage(request):
    """
    It takes a request, renders the homepage.html template, and passes the username of the user who made
    the request to the template
    """
    return render(request, 'Organizers\homepage.html', {"user_name": request.user.username})

@login_required(login_url='/login/  ')
def renderProfile(request):
    """
    It takes the user's information from the database and renders it on the profile page.
    """
    user_info={}
    user_db=myOrganizers.objects.get(pk=request.user.pk)
    user_info['username']=request.user.username
    user_info['email']=request.user.email
    user_info['Coname']=user_db.Company_name
    return render(request,'Organizers\profile.html',{"data":user_info})



@login_required(login_url='/login/  ')
def createEvents(request):
    if request.method=='POST':
        event_name_client=request.POST.get('eventname')
        event_date_client=request.POST.get('eventdate')
        event_max_capacity_client=request.POST.get('maxnumber')
        event_ticket_price_client=request.POST.get('price')
        event_place_client=request.POST.get('city')
        event_description_client=request.POST.get('desc')
        event_banner_client=request.FILES['eventimg']
        event_created=EventsCreated(event_organizer=request.user,event_name=event_name_client,event_date_time=event_date_client,event_maximum_capacity=event_max_capacity_client,event_ticket_price=event_ticket_price_client,event_place=event_place_client,event_description=event_description_client,number_of_current_guests=0,event_banner=event_banner_client)
        event_created.save()

        return render(request, 'Organizers\eventcreation.html')
    return render(request, 'Organizers\eventcreation.html')



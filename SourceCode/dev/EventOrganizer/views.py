from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from EventOrganizer.models import EventsCreated
# Create your views here.


@login_required(login_url='/login/  ')
def Get_homepage(request):
    return render(request, 'EventOrganizer\homepage.html', {"user_name": request.user.username})






@login_required(login_url='/login/  ')
def Get_profile_page(request):
    return render(request,'EventOrganizer\profile.html')



@login_required(login_url='/login/  ')
def Create_and_List_events(request):
    if request.method=='POST':
        event_name_client=request.POST.get('eventname')
        event_date_client=request.POST.get('eventdate')
        event_max_capacity_client=request.POST.get('maxnumber')
        event_ticket_price_client=request.POST.get('price')
        event_place_client=request.POST.get('city')
        event_description_client=request.POST.get('desc')
        event_banner_client=request.POST.get('eventimg')
        print(event_banner_client)
        event_created=EventsCreated(event_organizer=request.user,event_name=event_name_client,event_date_time=event_date_client,event_maximum_capacity=event_max_capacity_client,event_ticket_price=event_ticket_price_client,event_place=event_place_client,event_description=event_description_client,number_of_current_guests=0,event_banner=event_banner_client)
        event_created.save()
        return render(request, 'EventOrganizer\eventcreation.html')
    return render(request, 'EventOrganizer\eventcreation.html')

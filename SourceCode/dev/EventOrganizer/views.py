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
    event_name=request.POST.get('eventname')
    event_date=request.POST.get('eventdate')
    event_max_capacity=request.POST.get('maxnumber')
    event_ticket_price=request.POST.get('price')
    event_place=request.POST.get('city')
    event_description=request.POST.get('desc')
    event_created=EventsCreated(event_name,event_date,event_max_capacity,event_ticket_price,event_place,event_description,0)
    event_created.save()
    return render(request, 'EventOrganizer\eventcreation.html')

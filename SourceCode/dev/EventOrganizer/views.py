from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from EventOrganizer.models import EventsCreated
from SignUpAuth.models import Organizers
# Create your views here.


@login_required(login_url='/login/  ')
def Get_homepage(request):
    return render(request, 'EventOrganizer\homepage.html', {"user_name": request.user.username})






@login_required(login_url='/login/  ')
def Get_profile_page(request):
    user_info={}
    user_db=Organizers.objects.get(pk=request.user.pk)
    user_info['username']=request.user.username
    user_info['email']=request.user.email
    user_info['Coname']=user_db.company_name
    return render(request,'EventOrganizer\profile.html',{"data":user_info})



@login_required(login_url='/login/  ')
def Create_and_List_events(request):
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
        return render(request, 'EventOrganizer\eventcreation.html')
    return render(request, 'EventOrganizer\eventcreation.html')


@login_required(login_url='/login/  ')
def Get_Marketplace_Page(request):
    list_of_all_events=EventsCreated.objects.all()
    all_events=[]
    event={}
    for eve in list_of_all_events:
        event['id']=eve.pk
        event['name']=eve.event_name
        event['date/time']=eve.event_date_time
        event['desc']=eve.event_description
        event['banner']=eve.event_banner
        event['price']=eve.event_ticket_price
        event['maxcap']=eve.event_maximum_capacity
        event['available_places']=eve.event_maximum_capacity-eve.number_of_current_guests
        event['organizer']=eve.event_organizer
        all_events.append(event)
        event={}
    return render(request,'EventOrganizer\Marketplace.html',{'all_events':all_events})
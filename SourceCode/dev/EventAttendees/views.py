from django.shortcuts import render
from EventOrganizer.models import EventsCreated
# Create your views here.
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
def Get_homepage(request):
    return render(request, 'EventAttendees\homepage.html', {"user_name": request.user.username})



@login_required(login_url='/login/  ')
def Get_profile_page(request):
    return render(request,'EventAttendees\profile.html')



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
    return render(request,'EventAttendees\Marketplace.html',{'all_events':all_events})


@login_required(login_url='/login/  ')
def Get_specific_event_page(request,event_id):
    event_query=EventsCreated.objects.get(pk=event_id)
    event={}
    event['id']=event_query.pk
    event['name']=event_query.event_name
    event['datetime']=str(event_query.event_date_time)
    event['desc']=event_query.event_description
    event['banner']=event_query.event_banner
    event['price']=event_query.event_ticket_price
    event['available_places']=event_query.event_maximum_capacity-event_query.number_of_current_guests
    event['organizer']=event_query.event_organizer.username
    print(event)
    return render(request,'EventAttendees\event_info_page.html',{'all_events':event})



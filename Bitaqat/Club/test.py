from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .models import myUsers
from Club.models import myClub, Event, ClubsData, MintedTickets
from eth_account import Account
import secrets


def create_wallet():
    """
    Create a real crypto wallet.

    :return: The private key and the address of the account.
    """
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return private_key, acct.address


class ClubBrowsingPageTest(TestCase):
    def setUp(self):
        self.pwd = "Jihad2002"
        self.user = myUsers.objects.create(
            username="Alittihadfc",
            email="ittihad@test.com",
            password=make_password(self.pwd)
        )
        self.user.save()
        self.assertEqual(myUsers.objects.count(), 1)
        self.club_info = ClubsData.objects.create(
            name="ittihad",
            logo="/logo.png"
        )

        self.club_info2 = ClubsData.objects.create(
            name="Al Nassr FC",
            logo="/logo.png"
        )
        self.club_info2.save()

        self.club_info3 = ClubsData.objects.create(
            name="Al Fateh",
            logo="/logo.png"
        )
        self.club_info3.save()

        self.club_info4 = ClubsData.objects.create(
            name="Al Tai",
            logo="/logo.png"
        )
        self.club_info4.save()
        self.club = myClub.objects.create(
            user=self.user,
            club=self.club_info,
            RoyaltyReceiverAddresse="0x0b38E736326F6aB5F60C3eac7af19865A35fd205"
        )
        self.club.save()

    def test_view_url_exists_at_desired_location_homepage(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        response = self.client.get("/org/homepage/")
        self.assertEqual(response.status_code, 200)

    def test_views_uses_correct_template_homepage(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        response = self.client.get(reverse("Club:renderHomepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Club/HOME.html')

    def test_view_url_accessible_by_name_homepage(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        response = self.client.get(reverse("Club:renderHomepage"))
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_createEvent(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        response = self.client.get("/org/create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_createEvent(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        response = self.client.get(reverse("Club:createEvents"))
        self.assertEqual(response.status_code, 200)

    def test_views_uses_correct_template_eventcreation(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        response = self.client.get(reverse("Club:createEvents"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Club/eventcreation.html')

    def test_event_creation(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        team2_name2 = "Al Nassr FC"
        game_max_capacity_client = 100
        game_ticket_price_client = 45
        game_place_client = "Saudi Stadium"
        royalty = 10
        datetime = "2023-07-15 14:30:00"
        banner = "/team1.png"

        response = self.client.post(reverse("Club:createEvents"), data={
            'team': team2_name2,
            'maxnumber': game_max_capacity_client,
            'price': game_ticket_price_client,
            'city': game_place_client,
            'royap': royalty,
            'date': datetime,
            'banner': banner,
            "maxnumberticket": 3
        })
        obj = Event.objects.last()
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(team2_name2, obj.opposite_team.name)
        self.assertEqual(game_max_capacity_client, obj.maximum_capacity)
        self.assertEqual(game_ticket_price_client, obj.ticket_price)
        self.assertEqual(royalty, obj.royalty_rate)
        self.assertEqual(3, obj.maximum_ticket_per_account)


class AnalyticsTest(TestCase):
    def setUp(self):
        self.pwd = "Jihad2002"
        self.user = myUsers.objects.create(
            username="Alittihadfc",
            email="ittihad@test.com",
            password=make_password(self.pwd)
        )
        self.user.save()

        self.club_info = ClubsData.objects.create(
            name="ittihad",
            logo="/logo.png"
        )

        self.club_info2 = ClubsData.objects.create(
            name="Al Nassr FC",
            logo="/logo.png"
        )
        self.club_info2.save()

        self.club_info3 = ClubsData.objects.create(
            name="Al Fateh",
            logo="/logo.png"
        )
        self.club_info3.save()

        self.club_info4 = ClubsData.objects.create(
            name="Al Tai",
            logo="/logo.png"
        )
        self.club_info4.save()
        self.club = myClub.objects.create(
            user=self.user,
            club=self.club_info,
            RoyaltyReceiverAddresse="0x0b38E736326F6aB5F60C3eac7af19865A35fd205"
        )
        self.club.save()

        # create event 1
        self.event1 = Event.objects.create(
            organizer=self.club,
            datetime="2023-06-30 23:01",
            place="Beirut",
            maximum_capacity=200,
            maximum_ticket_per_account=3,
            ticket_price=50,
            current_fan_count=120,
            royalty_rate=10,
            banner="/logo.png",
            opposite_team=self.club_info2
        )
        self.event1.save()

        print(self.event1.pk)

        # create event 2
        self.event2 = Event.objects.create(
            organizer=self.club,
            datetime="2023-07-04 23:01",
            place="Beirut",
            maximum_capacity=200,
            maximum_ticket_per_account=3,
            ticket_price=20,
            current_fan_count=100,
            royalty_rate=10,
            banner="/logo.png",
            opposite_team=self.club_info3
        )
        self.event2.save()

        # create event 3
        self.event3 = Event.objects.create(
            organizer=self.club,
            datetime="2023-07-30 23:01",
            place="Beirut",
            maximum_capacity=200,
            maximum_ticket_per_account=3,
            ticket_price=150,
            current_fan_count=20,
            royalty_rate=10,
            banner="/logo.png",
            opposite_team=self.club_info4
        )
        self.event3.save()

        # Create 120 Fan
        self.list_of_fans = []
        for fannumber in range(0, 120):

            fan1 = myUsers.objects.create(
                username="fan"+str(fannumber),
                email="fan"+str(fannumber)+"@test.com",
                password=make_password(self.pwd)
            )
            fan1.save()
            self.list_of_fans.append(fan1)

        # Create 120 wallet
        self.list_of_wallets = []
        for user in range(0, 120):
            self.list_of_wallets.append(create_wallet()[1])

        # create 120 ticket minted for event 1
        self.list_of_tickets1 = []
        for ticketnumber in range(0, 120):
            ticketsMinted = MintedTickets.objects.create(
                event=self.event1,
                owner_account=self.list_of_fans[ticketnumber],
                owner_crypto_address=self.list_of_wallets[ticketnumber],
                token_id=ticketnumber,
                organizer=self.club,
            )
            ticketsMinted.save()
            self.list_of_tickets1.append(ticketsMinted)

        # create 120 ticket minted for event 2
        self.list_of_tickets2 = []
        for ticketnumber in range(120, 220):
            ticketsMinted = MintedTickets.objects.create(
                event=self.event2,
                owner_account=self.list_of_fans[ticketnumber-120],
                owner_crypto_address=self.list_of_wallets[ticketnumber-120],
                token_id=ticketnumber,
                organizer=self.club,
            )
            ticketsMinted.save()
            self.list_of_tickets2.append(ticketsMinted)

        # create 120 ticket minted for event 3
        self.list_of_tickets3 = []
        for ticketnumber in range(220, 240):
            ticketsMinted = MintedTickets.objects.create(
                event=self.event3,
                owner_account=self.list_of_fans[ticketnumber-220],
                owner_crypto_address=self.list_of_wallets[ticketnumber-220],
                token_id=ticketnumber,
                organizer=self.club,
            )
            ticketsMinted.save()
            self.list_of_tickets3.append(ticketsMinted)

    def test_renderAnalytics_view(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        response = self.client.get(reverse("Club:myEvents"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Club\Dashboard.html')
        self.assertEqual(response.context['rev'], 5000)
        self.assertAlmostEqual(response.context['delta'], -16.67)
        self.assertEqual(response.context['att'], 40)
        self.assertEqual(response.context['pg']
                         [0]['opposite_team']['name'], "Al Nassr FC")
        self.assertEqual(response.context['pg']
                         [1]['opposite_team']['name'], "Al Tai")
        self.assertEqual(response.context['pg']
                         [2]['opposite_team']['name'], "Al Fateh")
        self.assertEqual(
            int(response.context['transaction'][1]["token_id"]), int(self.list_of_tickets3[-1].token_id))
        self.assertEqual(response.context['bestevent']
                         ['name'], "Al Nassr FC")
        self.assertEqual(response.context['numberoftickets'], 240)
        self.assertEqual(response.context['totalrevenue'], 11000)
        self.assertEqual(len(response.context['games']), 3)

    def test_event_dashboard_view(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        response = self.client.get("/org/MyGame/4/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Club/myGame.html')
        self.assertEqual(len(response.context['eventData']), 120)
        print(response.context['Data'][0].current_fan_count)
        self.assertEqual(response.context['Data'][0].current_fan_count
                         * response.context['Data'][0].ticket_price, 120*50)

        response2 = self.client.get("/org/MyGame/5/")
        self.assertEqual(len(response2.context['eventData']), 100)
        self.assertEqual(response2.context['Data'][0].current_fan_count
                         * response2.context['Data'][0].ticket_price, 100*20)

        response3 = self.client.get("/org/MyGame/6/")
        self.assertEqual(len(response3.context['eventData']), 20)
        self.assertEqual(response3.context['Data'][0].current_fan_count
                         * response3.context['Data'][0].ticket_price, 150*20)

    def test_qrCodeScanView(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        response = self.client.get(reverse("Club:qrCodeScanView"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Club\qr_code_scan.html")

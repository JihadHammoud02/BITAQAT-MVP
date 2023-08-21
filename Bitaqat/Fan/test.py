from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .models import myUsers
from Club.models import myClub, Event, ClubsData, MintedTickets
from eth_account import Account
import secrets
from Fan.models import myFan
import time
from Fan.views import match_address_with_account, count_tickets_in_accounts


def create_wallet():
    """
    Create a real crypto wallet.

    :return: The private key and the address of the account.
    """
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return private_key, acct.address


class FanBrowsingPageTest(TestCase):
    def setUp(self):
        self.pwd = "Jihad2002"
        self.myfan = myUsers.objects.create(
            username="Jihad",
            email="Jihadhammoud@gmail.com",
            password=make_password(self.pwd)
        )

        self.myfan.save()
        print("This is "+str(self.myfan.pk))
        wallet = create_wallet()

        self.fan_acc = myFan.objects.create(
            user=self.myfan,
            public_key=wallet[1],
            private_key=wallet[0]
        )
        self.fan_acc.save()

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
            maximum_capacity=120,
            maximum_ticket_per_account=3,
            ticket_price=50,
            current_fan_count=120,
            royalty_rate=10,
            banner="/logo.png",
            opposite_team=self.club_info2
        )
        self.event1.save()

        # create event 2
        self.event2 = Event.objects.create(
            organizer=self.club,
            datetime="2024-08-03 23:01",
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
            datetime="2024-07-30 23:01",
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

        ticketsMinted1 = MintedTickets.objects.create(
            event=self.event3,
            owner_account=self.myfan,
            owner_crypto_address=self.fan_acc.public_key,
            token_id=241,
            organizer=self.club,
        )
        ticketsMinted1.save()
        print("bought1")

        ticketsMinted2 = MintedTickets.objects.create(
            event=self.event2,
            owner_account=self.myfan,
            owner_crypto_address=self.fan_acc.public_key,
            token_id=242,
            organizer=self.club,
        )
        ticketsMinted2.save()

        ticketsMinted3 = MintedTickets.objects.create(
            event=self.event3,
            owner_account=self.myfan,
            owner_crypto_address=self.fan_acc.public_key,
            token_id=343,
            organizer=self.club,
        )
        ticketsMinted3.save()

    def test_view_url_exists_at_desired_location_homepage(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        response = self.client.get("/guest/Marketplace/")
        self.assertEqual(response.status_code, 200)

    def test_views_uses_correct_template_homepage(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        response = self.client.get(reverse("Fan:renderHomepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Fan/HOME.html')

    def test_view_url_exists_at_desired_location_marketplace(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        response = self.client.get("/guest/Marketplace/")
        self.assertEqual(response.status_code, 200)

    def test_views_uses_correct_template_homepage(self):
        login = self.client.login(
            username=self.user.username, password=self.pwd)
        response = self.client.get(reverse("Fan:renderMarketplace"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Fan\GAMES.html')

    def test_render_Marketplace(self):
        login = self.client.login(
            username=self.myfan, password=self.pwd)
        response = self.client.get(reverse("Fan:renderMarketplace"))
        self.assertEqual(len(response.context['all_events']), 2)

    def test_match_address_with_account(self):
        self.assertEqual(match_address_with_account(
            self.fan_acc.public_key).pk, self.myfan.pk)

    def test_count_tickets_in_accounts(self):
        self.assertEqual(count_tickets_in_accounts(
            1, self.event3), 2)

    def test_renderInventory(self):
        login = self.client.login(
            username=self.myfan, password=self.pwd)
        response = self.client.get(reverse("Fan:renderMarketplace"))
        self.assertEqual(len(response.context['collection']), 3)

    def test_renderKeys(self):
        login = self.client.login(
            username=self.myfan, password=self.pwd)
        response = self.client.get(reverse("Fan:Mykeys"))
        self.assertEqual(response.context['pk'], self.fan_acc.private_key)
        self.assertEqual(
            response.context['publickey'], self.fan_acc.public_key)

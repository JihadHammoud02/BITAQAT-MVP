from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .models import myUsers
from Club.models import myClub
from Fan.models import myFan


class LandingPageTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_login(self):
        response = self.client.get(reverse("authentication:landingPage"))
        self.assertEqual(response.status_code, 200)

    def test_views_uses_correct_template(self):
        response = self.client.get(reverse('authentication:landingPage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/landingPage.html')


class authenticationTest(TestCase):
    def setUp(self):
        pass

    def test_view_url_exists_at_desired_location_login(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_login(self):
        response = self.client.get(reverse("authentication:loginmyUsers"))
        self.assertEqual(response.status_code, 200)

    def test_views_uses_correct_template_login(self):
        response = self.client.get(reverse('authentication:loginmyUsers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/Login.html')

    def test_view_url_exists_at_desired_location_signup(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_signup(self):
        response = self.client.get(reverse("authentication:createAccounts"))
        self.assertEqual(response.status_code, 200)

    def test_views_uses_correct_template_signup(self):
        response = self.client.get(reverse('authentication:createAccounts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/Registration.html')

    def test_fan_creation_account_and_login(self):
        response = self.client.post(reverse("authentication:createAccounts"), data={
            'username': "Jihad2",
            "emailadd": "jihad@gmail.com",
            "pswrd": "Jihad2002"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(myUsers.objects.count(), 1)
        self.assertEqual(myFan.objects.count(), 1)
        response = self.client.post(reverse("authentication:loginmyUsers"), data={
            'username': "Jihad2",
            "pswrd": "Jihad2002"
        })
        self.assertEqual(response.status_code, 302)

    def test_club_login(self):
        pwd = "Jihad2002"
        user = myUsers.objects.create(
            username="Alittihadfc",
            email="ittihad@test.com",
            password=make_password(pwd)
        )
        user.save()
        self.assertEqual(myUsers.objects.count(), 1)
        club_info = myClub.objects.create(
            name="ittihad",
            logo="/logo.png"
        )
        club_info.save()
        club = myClub.objects.create(
            user=user,
            club=club_info,
            RoyaltyReceiverAddresse="0x0b38E736326F6aB5F60C3eac7af19865A35fd205"
        )
        club.save()
        self.assertEqual(myClub.objects.count(), 1)
        response = self.client.post(reverse("authentication:loginmyUsers"), data={
            'username': user.username,
            "pswrd": pwd
        })
        self.assertEqual(response.status_code, 302)

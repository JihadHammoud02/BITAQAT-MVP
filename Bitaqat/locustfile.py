from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 3)
    # Replace with the URL of your Django app
    host = "http://your-django-app-domain/"

    @task
    def buy_ticket(self):
        # Replace 'event_id' with the specific event_id you want to test
        event_id = 1  # Modify this to the desired event_id

        # Access the /login/ page first to get the CSRF token
        response = self.client.get("/login/")
        # Extract the CSRF token from the cookies
        csrf_token = response.cookies['csrftoken']

        # Simulate login using valid credentials or use the ones created during account creation
        login_payload = {
            "username": "Jihad",
            "pswrd": "Jihad2002",
            "csrfmiddlewaretoken": csrf_token,  # Include CSRF token in the payload
        }
        self.client.post("/login/", data=login_payload)

        # Prepare the payload for the POST request to buyTicket
        buy_ticket_payload = {
            "csrfmiddlewaretoken": csrf_token,  # Include CSRF token in the payload
        }

        # Make the POST request to the buyTicket endpoint
        response = self.client.post(
            f"/guest/Buy/37/", data=buy_ticket_payload)

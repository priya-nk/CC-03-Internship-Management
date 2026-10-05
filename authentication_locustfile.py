from locust import HttpUser, task, between

class AuthenticatedUser(HttpUser):
    wait_time = between(0.1, 0.5)
    token = None

    def on_start(self):
        """
        Runs automatically ONCE for every simulated user when spawned.
        Logs in and stores the access token in headers.
        """
        login_payload = {
            "username": "testuser",
            "password": "testpassword"
        }
        
        # Enable catch_response=True inside a 'with' block
        with self.client.post("/auth/login", json=login_payload, catch_response=True) as response:
            if response.status_code == 200:
                token_data = response.json()
                self.token = token_data.get("access_token")
                # Set Authorization header for all subsequent HTTP calls
                self.client.headers.update({"Authorization": f"Bearer {self.token}"})
            else:
                response.failure(f"Failed to authenticate user: {response.status_code}")


    @task(1)
    def test_health_check(self):
        self.client.get("/")
from locust import HttpUser, task, between
import json
import random
import logging

class EventLoadTest(HttpUser):
    host = "https://mock-api.rrvs.my.id"

    wait_time = between(1, 5)

    @task
    def create_event(self):
        endpoint = "/auth/register"

        payload = {
            "name": "Test2",
            "email": "tests2@example.com",
            "password": "password0123"
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        with self.client.post(endpoint, data=json.dumps(payload), headers=headers, catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 201:
                response.success()
                logging.info(f"Berhasil! Response API: {response.text}")
            else:
                response.failure(f"Failed! Status code: {response.status_code}, Response: {response.text}")
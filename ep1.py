from locust import HttpUser, task, between
import json
import random
import logging

class EventLoadTest(HttpUser):
    # Host utama (tanpa path endpoint)
    host = "https://everlasting-api.ourmoment.my.id"

    # Waktu jeda antara setiap request per user (1 sampai 5 detik)
    wait_time = between(1, 5)

    @task
    def create_event(self):
        endpoint = "/api/v1/event"

        # Dummy data untuk payload (bisa disesuaikan atau dibuat random)
        payload = {
            "title": "asdad",
            "description": "asdadasd",
            "date": "2026-07-02T00:00:00Z",
            "time": "1000",
            "location": "Blok",
            "category": "blok",
            "max_messages": 200,
            "status": "active",
            "organizer": "string (required)"
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Melakukan POST request dan menangkap response
        with self.client.post(endpoint, data=json.dumps(payload), headers=headers, catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 201:
                response.success()
                logging.info(f"Berhasil! Response API: {response.text}")
            else:
                response.failure(f"Failed! Status code: {response.status_code}, Response: {response.text}")
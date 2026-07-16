from locust import HttpUser, task, between
import json
# import random
import logging

class EventLoadTest(HttpUser):
    host = "https://mock-api.rrvs.my.id"

    # wait_time = between(1, 5)
    bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI1OWI1ODNiNi1jNTIyLTQ2NTQtODhkMS03OGRjNTZjMTcxNTciLCJlbWFpbCI6IlRlc3QzQGV4YW1wbGUuY29tIiwiaWF0IjoxNzg0MjEyMTYyLCJleHAiOjE3ODQyMTU3NjJ9.wGDqYO0iE17bbbLB5zTfCZQR_6B20bPhnpoK8SDMtG0"

    @task
    def create_event(self):
        endpoint = "/projects"

        payload = {
            "name": "Project 1"
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.bearer_token}"
        }

        with self.client.post(endpoint, data=json.dumps(payload), headers=headers, catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 201:
                response.success()
                logging.info(f"Berhasil! Response API: {response.text}")
            else:
                response.failure(f"Failed! Status code: {response.status_code}, Response: {response.text}")
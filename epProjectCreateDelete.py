from locust import HttpUser, task, between
import json
import random
import logging


class EventLoadTest(HttpUser):
    host = "https://mock-api.rrvs.my.id"

    wait_time = between(1, 5)

    bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI1OWI1ODNiNi1jNTIyLTQ2NTQtODhkMS03OGRjNTZjMTcxNTciLCJlbWFpbCI6IlRlc3QzQGV4YW1wbGUuY29tIiwiaWF0IjoxNzg0MjE1NzIxLCJleHAiOjE3ODQyMTkzMjF9.l3OL6YkXbSe0nbuvyuf7fQPJU_BzqO4MZ_JDVC0VSFE"

    @task
    def create_event(self):
        endpoint = "/projects/fb4534bd-dff7-4f3d-8c46-2ad6b03f536d/tasks"

        random_id = random.randint(100, 9999)

        payload = {
            "title": f"Task {random_id}"
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.bearer_token}"
        }

        with self.client.post(
            endpoint,
            data=json.dumps(payload),
            headers=headers,
            catch_response=True,
            name="POST /tasks"
        ) as response:

            if response.status_code in [200, 201]:
                response.success()
                logging.info(f"POST Success: {response.text}")

                try:
                    response_json = response.json()
                    task_id = (
                        response_json.get("id")
                        or response_json.get("data", {}).get("id")
                    )

                    if task_id:
                        delete_headers = {
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "Authorization": f"Bearer {self.bearer_token}"
                        }

                        delete_url = f"/tasks/{task_id}"

                        with self.client.delete(
                            delete_url,
                            headers=delete_headers,
                            catch_response=True,
                            name="DELETE /tasks/[id]"
                        ) as delete_response:

                            if delete_response.status_code in [200, 202, 204]:
                                delete_response.success()
                                logging.info(f"DELETE Success: {task_id}")
                            else:
                                delete_response.failure(
                                    f"Gagal DELETE: {delete_response.status_code} - {delete_response.text}"
                                )

                    else:
                        response.failure(
                            f"POST berhasil tetapi task id tidak ditemukan.\n{response.text}"
                        )

                except ValueError:
                    response.failure(
                        "POST berhasil tetapi response bukan JSON yang valid."
                    )

            else:
                response.failure(
                    f"POST gagal: {response.status_code} - {response.text}"
                )
from locust import HttpUser, task, between

class BeeceptorLoadTest(HttpUser):
    # Base URL dari target testing Anda
    host = "https://sinarmas-va-e2e.free.beeceptor.com"
    
    # Simulasi jeda waktu (delay) antar request untuk setiap user, antara 1 - 3 detik
    wait_time = between(1, 3)

    @task
    def hit_test_endpoint(self):
        # Memanggil path /test menggunakan HTTP GET
        # Ubah self.client.get menjadi self.client.post jika target berupa endpoint POST
        with self.client.get("/test", catch_response=True) as response:
            
            # (Opsional) Validasi sederhana apakah request berhasil
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Gagal! Status code: {response.status_code}")
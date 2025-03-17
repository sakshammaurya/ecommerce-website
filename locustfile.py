from locust import HttpUser, task, between

class EcommerceUser(HttpUser):
    wait_time = between(1, 5)  # Simulates user delay

    @task(3)
    def browse_products(self):
        self.client.get("/products/")  # Adjust endpoint as per your Django setup

    @task(2)
    def view_product(self):
        self.client.get("/products/1/")  # Simulate viewing a specific product

    @task(1)
    def add_to_cart(self):
        self.client.post("/cart/add/", json={"product_id": 1, "quantity": 1})

    @task(1)
    def checkout(self):
        self.client.post("/checkout/", json={"payment_method": "card"})


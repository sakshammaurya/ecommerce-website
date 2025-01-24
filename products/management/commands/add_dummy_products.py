import random
import os
import requests

from django.core.management.base import BaseCommand
from products.models import Product  # Replace 'myapp' with your app's name
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Add 100 dummy products to the database with images'

    def download_random_image(self, image_number):
        """Download a random image from the web."""
        url = f"https://picsum.photos/200/300?random={image_number}"
        image_path = f"media/product_images/dummy_product_{image_number}.jpg"

        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(image_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return image_path
        else:
            return None

    def handle(self, *args, **kwargs):
        categories = ['Electronics', 'Fashion', 'Home', 'Books', 'Toys']
        for i in range(100):
            image_path = self.download_random_image(i + 1)
            if image_path:
                product = Product(
                    name=f"Dummy Product {i+1}",
                    description=f"This is a detailed description for Dummy Product {i+1}.",
                    price=round(random.uniform(10.0, 500.0), 2),  # Random price between 10 and 500
                    stock_quantity=random.randint(1, 100),  # Random stock between 1 and 100
                    category=random.choice(categories),  # Random category
                    image_url=image_path,  # Assuming your Product model has an 'image' field
                    created_at=now(),
                    updated_at=now()
                )
                product.save()

        self.stdout.write(self.style.SUCCESS('Successfully added 100 dummy products with images.'))

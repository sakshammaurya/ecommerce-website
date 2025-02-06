# products/migrations/0002_add_dummy_data.py
from django.db import migrations
from django.utils.text import slugify
from faker import Faker
import requests
from io import BytesIO
from django.core.files import File
import time

fake = Faker()

def generate_categories_and_products(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Product = apps.get_model('products', 'Product')
    

    # Delete existing data (optional)
    #OrderItem.objects.all().delete()
    #Product.objects.all().delete()
    #Category.objects.all().delete()

    # Create categories
    for cat_num in range(1, 101):
        category_name = f"Category {cat_num}"
        category_slug = slugify(category_name)
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'slug': category_slug}
        )
        if created:
            print(f"Created category: {category_name}")

        # Create products
        for prod_num in range(1, 101):
            product_name = f"Product {prod_num} in {category_name}"
            product = Product(
                name=product_name,
                description=fake.paragraph(),
                price=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
                stock_quantity=fake.random_int(min=0, max=1000),
                stock_status=fake.random_element(elements=(0, 1, 2)),
                category=category
            )

            # Add image (with error handling)
            try:
                image_url = f"https://placehold.co/600x400/EEE/31343C?text={product_name.replace(' ', '+')}"
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    image_name = f"product_{prod_num}_cat_{cat_num}.png"
                    product.image.save(image_name, File(BytesIO(response.content)), save=False)
                else:
                    print(f"Failed to download image for {product_name}")
            except Exception as e:
                print(f"Error downloading image: {e}")

            product.save()
            print(f"Created product: {product_name}")

class Migration(migrations.Migration):
    atomic = False  # Disable transactions to avoid rollback
    dependencies = [
        ('products', '0002_add_dummy_data'),
    ]

    operations = [
        migrations.RunPython(generate_categories_and_products),
    ]
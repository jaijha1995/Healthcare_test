import os
import django

# ✅ Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restserver.settings")  # Replace with your actual settings module
django.setup()

from Product.models import Product  # Update with your actual app name if different
from faker import Faker
import random
from tqdm import tqdm
from decimal import Decimal

fake = Faker()

# ✅ Configuration
total_records = 1000000  # 10 lakh
batch_size = 1000

PRODUCT_TYPE_CHOICES = [
    "TOP_RATED",
    "NEW_ARRIVALS",
    "BEST_SELLERS",
    "Most Popular Products",
    "Trending Products",
]

SECTIONS = ['Men', 'Women', 'Kids', 'Accessories', 'Footwear']
GENDERS = ['male', 'female', 'unisex']

print("🚀 Creating 10 lakh fake product records...")

for i in tqdm(range(0, total_records, batch_size), desc="Inserting Products"):
    products = []
    for _ in range(batch_size):
        title_types = random.choice(PRODUCT_TYPE_CHOICES)
        # ✅ Safe and unique-like name generation
        name = f"{fake.word().capitalize()} {fake.word().capitalize()} {random.randint(1000, 999999)}"
        description = fake.paragraph(nb_sentences=5)
        price = Decimal(random.uniform(10.0, 999.99)).quantize(Decimal('0.01'))
        in_stock = fake.boolean(chance_of_getting_true=80)
        gender = random.choice(GENDERS)
        image = fake.image_url()
        model_3d = fake.url()
        size_tags = {
            "sizes": random.sample(["XS", "S", "M", "L", "XL"], k=random.randint(1, 5))
        }
        is_active = fake.boolean(chance_of_getting_true=95)
        dfx_content = {
            "colors": random.sample(["red", "blue", "green", "black", "white"], k=random.randint(1, 3))
        }
        section = random.choice(SECTIONS)

        products.append(Product(
            title_types=title_types,
            name=name,
            description=description,
            price=price,
            in_stock=in_stock,
            gender=gender,
            image=image,
            model_3d=model_3d,
            size_tags=size_tags,
            is_active=is_active,
            dfx_content=dfx_content,
            section=section
        ))

    # ✅ Batch insert
    Product.objects.bulk_create(products, batch_size=batch_size)

print("✅ 10 lakh product records created successfully.")

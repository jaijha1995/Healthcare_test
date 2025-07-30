import os
import django
import random
from faker import Faker
from tqdm import tqdm
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restserver.settings")
django.setup()

from Product.models import Product  # Replace with your actual app and model if different

# Initialize Faker
fake = Faker()

# Parameters
batch_size = 5000
total_records = 100000

# Product field choices
PRODUCT_TYPE_CHOICES = [
    "TOP_RATED", "NEW_ARRIVALS", "BEST_SELLERS", "MOST_POPULAR", "TRENDING"
]
GENDER_CHOICES = ["MALE", "FEMALE", "UNISEX", None]
SECTIONS = ["Men", "Women", "Kids", "Accessories", None]
SIZES = ["S", "M", "L", "XL", "XXL"]

print(f"🚀 Starting creation of {total_records} fake Product records...")

# Generate and insert products in batches
for _ in tqdm(range(0, total_records, batch_size), desc="Inserting Products"):
    products = []

    for _ in range(batch_size):
        name = f"{fake.word().capitalize()} Product"
        description = fake.text(max_nb_chars=200)
        price = round(random.uniform(10, 1000), 2)
        in_stock = random.choice([True, False])
        gender = random.choice(GENDER_CHOICES)
        image = fake.image_url()
        model_3d = fake.url()
        size_tags = random.sample(SIZES, k=random.randint(1, 3))
        is_active = random.choice([True, False])
        dfx_content = {"material": fake.word(), "color": fake.color_name()}
        section = random.choice(SECTIONS)
        title_type = random.choice(PRODUCT_TYPE_CHOICES)

        product = Product(
            name=name,
            description=description,
            price=Decimal(price),
            in_stock=in_stock,
            gender=gender,
            image=image,
            model_3d=model_3d,
            size_tags=size_tags,
            is_active=is_active,
            dfx_content=dfx_content,
            section=section,
            title_types=title_type
        )
        products.append(product)

    Product.objects.bulk_create(products)

print("✅ Done. Successfully inserted 1 lakh Product records.")

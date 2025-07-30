import os
import django
import random
from faker import Faker
from tqdm import tqdm

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restserver.settings")
django.setup()

from virtual_model.models import Category, SubCategory, SubSubCategory


fake = Faker()
RECORDS_PER_TYPE = 10000

def insert_fake_data(model, type_value, total):
    print(f"🔄 Inserting {total} records into {type_value}...")

    from django.db import transaction
    with transaction.atomic():
        for _ in tqdm(range(total), desc=f"Seeding {type_value}"):
            name = f"{fake.word().capitalize()}_{random.randint(1000, 9999)}"
            model.objects.create(
                name=name,
                type=type_value
            )

def run():
    print("🧹 Deleting existing data in Category table...")
    Category.objects.all().delete()

    insert_fake_data(Category, 'category', RECORDS_PER_TYPE)
    insert_fake_data(SubCategory, 'subcategory', RECORDS_PER_TYPE)
    insert_fake_data(SubSubCategory, 'subsubcategory', RECORDS_PER_TYPE)

    print("✅ Fake data inserted successfully into Category table.")

if __name__ == "__main__":
    run()

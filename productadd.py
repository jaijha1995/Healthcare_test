import os
import django
from faker import Faker
from tqdm import tqdm

# ✅ Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restserver.settings")  # Replace with your Django project settings
django.setup()

from virtual_model.models import Category, SubCategory, SubSubCategory  # Replace with your actual app name

# ✅ Configurations
TOTAL_PER_TYPE = 1000  # You can increase this if needed
fake = Faker()

def create_fake_entries(model_class, type_name, total):
    print(f"🚀 Creating {total} fake records for: {type_name}")
    from django.db import transaction

    with transaction.atomic():
        for _ in tqdm(range(total), desc=f"Seeding {type_name}"):
            model_class.objects.create(
                name=fake.unique.word().capitalize(),
                type=type_name
            )

def run_seed():
    # Delete existing data if needed
    print("🧹 Clearing existing Category data...")
    Category.objects.all().delete()

    # Insert fake data into all 3 types
    create_fake_entries(Category, "category", TOTAL_PER_TYPE)
    create_fake_entries(SubCategory, "subcategory", TOTAL_PER_TYPE)
    create_fake_entries(SubSubCategory, "subsubcategory", TOTAL_PER_TYPE)

    print("✅ All fake categories created successfully.")

if __name__ == "__main__":
    run_seed()

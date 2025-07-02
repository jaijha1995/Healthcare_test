# If running as a standalone script, uncomment the lines below:
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restserver.settings")  # Replace with your actual project name
django.setup()

from contact.models import Contact  # ✅ Assuming app name is `contact`
from faker import Faker
import random
from tqdm import tqdm

fake = Faker()

# ✅ Config
total_records = 100000
batch_size = 1000

print("🚀 Creating fake contact records...")

for i in tqdm(range(0, total_records, batch_size), desc="Creating contacts"):
    contacts = []
    for _ in range(batch_size):
        name = fake.name()
        email = fake.unique.email()
        mobile = fake.unique.msisdn()[0:10]
        message = fake.paragraph(nb_sentences=3)

        contacts.append(Contact(
            name=name,
            email=email,
            mobile=mobile,
            message=message
        ))



    Contact.objects.bulk_create(contacts, batch_size=batch_size)

print("✅ 50,000 contacts created successfully.")

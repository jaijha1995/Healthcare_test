import os
import django
import random
from faker import Faker
from tqdm import tqdm

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restserver.settings")  # Replace with your settings module
django.setup()

from customer.models import Customer  # Replace with your actual app name
from superadmin.models import SuperAdmin

# Ensure SuperAdmin with ID=1 exists
if not SuperAdmin.objects.filter(id=1).exists():
    SuperAdmin.objects.create(
        id=1,
        name="Default Admin",
        email="admin@example.com",
        password="admin123"  # Plain text; hash if needed
    )
    print("✅ SuperAdmin with ID=1 created.")
else:
    print("ℹ️ SuperAdmin with ID=1 already exists.")

# Initialize Faker
fake = Faker()

# Parameters
batch_size = 5000
total_records = 100000
superadmin_id = 1

print(f"🚀 Starting creation of {total_records} fake customers...")

# Insert in batches
for _ in tqdm(range(0, total_records, batch_size), desc="Inserting Customers"):
    customers = []
    for _ in range(batch_size):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        mobile = fake.unique.msisdn()[0:10]
        password = "password123"
        otp = str(random.randint(1000, 9999))

        customer = Customer(
            superadmin_id=superadmin_id,
            name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            password=password,
            re_password=password,
            otp=otp,
            role='Customer',
            whatsapp=mobile
        )
        customers.append(customer)

    # Bulk insert
    Customer.objects.bulk_create(customers)

print("✅ Done. Successfully inserted 1 lakh customer records.")

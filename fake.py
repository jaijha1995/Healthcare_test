# If running as a standalone script, uncomment the lines below:
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restserver.settings")  # Replace with your actual project name
django.setup()

from customer.models import Customer
from superadmin.models import SuperAdmin
from faker import Faker
import random
from tqdm import tqdm  # Optional: progress bar

fake = Faker()

# Get SuperAdmin instance
superadmin = SuperAdmin.objects.first()
if not superadmin:
    raise Exception("❌ No SuperAdmin found. Please create one before running this script.")

# Config for next 50,000 records (from 50,000 to 100,000)
start = 50000
end = 100000
batch_size = 1000

for i in tqdm(range(start, end, batch_size), desc="Creating customers"):
    customers = []
    for _ in range(batch_size):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        mobile = fake.unique.msisdn()[0:10]
        password = fake.password(length=10)
        otp = str(random.randint(100000, 999999))

        customers.append(Customer(
            superadmin=superadmin,
            name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            password=password,
            otp=otp,
            role="Customer"
        ))

    Customer.objects.bulk_create(customers, batch_size)

print("✅ Customers 50,000 to 100,000 created successfully.")

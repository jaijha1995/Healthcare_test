import os
import django
import random
from faker import Faker

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restserver.settings")
django.setup()

from master_com.models import Order
from customer.models import Customer
from superadmin.models import SuperAdmin
from candidates.models import Candidate
from contact.models import Contact
from Product.models import Product
from virtual_model.models import Category, SubCategory, SubSubCategory

fake = Faker()

print("🚀 Preparing foreign key data...")

# Ensure ForeignKey tables have data
def seed_foreign_keys(min_count=5):
    # SuperAdmin must be seeded first (assume ID 1 needed)
    if SuperAdmin.objects.count() == 0:
        for _ in range(min_count):
            SuperAdmin.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                password="admin123"
            )

    superadmin = SuperAdmin.objects.first()

    for _ in range(min_count):
        Customer.objects.get_or_create(
            email=fake.unique.email(),
            defaults={
                'name': fake.first_name(),
                'last_name': fake.last_name(),
                'mobile': fake.unique.msisdn()[:10],
                'password': 'pass123',
                're_password': 'pass123',
                'otp': fake.random_number(digits=6),
                'role': 'Customer',
                'superadmin': superadmin,
                'whatsapp': fake.phone_number()
            }
        )

        Candidate.objects.get_or_create(
            email=fake.unique.email(),
            defaults={'name': fake.name(), 'phone': fake.phone_number()}
        )

        Contact.objects.get_or_create(
            email=fake.unique.email(),
            defaults={'name': fake.name(), 'mobile': fake.phone_number(), 'message': fake.text()}
        )

        Product.objects.get_or_create(
            name=fake.word(),
            defaults={'price': round(random.uniform(100, 5000), 2)}
        )

        category = Category.objects.create(name=fake.word(), type='category')
        subcategory = SubCategory.objects.create(name=fake.word(), type='subcategory', category=category)
        SubSubCategory.objects.create(name=fake.word(), type='subsubcategory', subcategory=subcategory)


seed_foreign_keys()

# Load related data into memory
customers = list(Customer.objects.all())
superadmins = list(SuperAdmin.objects.all())
candidates = list(Candidate.objects.all())
contacts = list(Contact.objects.all())
products = list(Product.objects.all())
categories = list(Category.objects.all())
subcategories = list(SubCategory.objects.all())
subsubcategories = list(SubSubCategory.objects.all())

order_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']

print("✅ Foreign key tables loaded.")
print("📦 Generating fake orders...")

# Fake Order creation loop
batch_size = 1000
total_to_create = 10000
total_created = 0

while total_created < total_to_create:
    orders_to_create = []
    for _ in range(min(batch_size, total_to_create - total_created)):
        orders_to_create.append(Order(
            customer=random.choice(customers),
            superadmin=random.choice(superadmins),
            candidate=random.choice(candidates),
            contact=random.choice(contacts),
            product=random.choice(products),
            category=random.choice(categories),
            subcategory=random.choice(subcategories),
            subsubcategory=random.choice(subsubcategories),
            order_status=random.choice(order_statuses),
            total_amount=round(random.uniform(100.00, 5000.00), 2),
        ))

    Order.objects.bulk_create(orders_to_create)
    total_created += len(orders_to_create)
    print(f"📝 {total_created} orders created...")

print(f"🎉 Done! Total fake orders created: {total_created}")

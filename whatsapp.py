import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restserver.settings")  # ✅ Replace with your project name
django.setup()

from customer.models import Customer

print("🚀 Updating all customers where whatsapp is NULL...")

batch_size = 1000
total_updated = 0

while True:
    # Always get the next batch of customers with null whatsapp
    customers = list(Customer.objects.filter(whatsapp__isnull=True)[:batch_size])
    
    if not customers:
        break  # All done

    for customer in customers:
        customer.whatsapp = customer.mobile

    Customer.objects.bulk_update(customers, ['whatsapp'])
    total_updated += len(customers)

    print(f"✔️ Updated {total_updated} customers so far...")

print(f"✅ Done. Total customers updated: {total_updated}")

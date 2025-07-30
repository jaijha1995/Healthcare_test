import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restserver.settings")  # Replace with your project name
django.setup()

from contact.models import Contact
from django.db.models import Q

print("🚀 Starting update: Setting `whatsapp = mobile` where `whatsapp` is NULL or empty...")

batch_size = 1000
total_updated = 0

while True:
    # Match NULL or empty whatsapp AND non-null/non-empty mobile
    contacts_to_update = list(Contact.objects.filter(
        Q(whatsapp__isnull=True) | Q(whatsapp='')
    ).exclude(mobile__isnull=True).exclude(mobile='')[:batch_size])

    print(f"🔍 Found {len(contacts_to_update)} contacts to update in this batch...")

    if not contacts_to_update:
        break

    for contact in contacts_to_update:
        contact.whatsapp = contact.mobile

    Contact.objects.bulk_update(contacts_to_update, ['whatsapp'])
    total_updated += len(contacts_to_update)

    print(f"✔️ Updated {total_updated} contacts so far...")

print(f"✅ Done. Total contacts updated: {total_updated}")

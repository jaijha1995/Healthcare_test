from django.contrib import admin
from .models import Order


from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Columns to display in the list view
    list_display = [
        'id', 'customer', 'order_status',
        'order_date', 'total_amount'
    ]

    # Filters in the right sidebar
    list_filter = ['order_status', 'order_date']

    # Search box fields
    search_fields = [
        'customer__name', 
        'contact__name', 
        'product__name'
    ]

    # Results per page
    list_per_page = 50

    # Default sorting
    ordering = ['-order_date']

    # Use raw ID input instead of dropdowns (speeds up large datasets)
    raw_id_fields = [
        'customer',
        'superadmin',
        'candidate',
        'contact',
        'product',
        'category',
        'subcategory',
        'subsubcategory',
    ]

    # Optimize foreign key queries to reduce DB hits
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'customer',
            'superadmin',
            'candidate',
            'contact',
            'product',
            'category',
            'subcategory',
            'subsubcategory'
        )

# Register your models here.
from django.db import models
from superadmin.models import SuperAdmin
from customer.models import Customer
from virtual_model.models import Category, SubCategory, SubSubCategory
from candidates.models import Candidate
from contact.models import Contact
from Product.models import Product


class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    superadmin = models.ForeignKey(SuperAdmin, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='orders_by_category')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='orders_by_subcategory')
    subsubcategory = models.ForeignKey(SubSubCategory, on_delete=models.CASCADE, related_name='orders_by_subsubcategory')

    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-order_date']
        db_table = 'order'
        unique_together = ('customer', 'order_date')
        indexes = [
            models.Index(fields=['order_date']),
            models.Index(fields=['order_status']),
            models.Index(fields=['total_amount']),
            models.Index(fields=['customer']),
            models.Index(fields=['superadmin']),
            models.Index(fields=['candidate']),
            models.Index(fields=['contact']),
            models.Index(fields=['product']),
            models.Index(fields=['category']),
            models.Index(fields=['subcategory']),
            models.Index(fields=['subsubcategory']),
        ]

    def __str__(self):
        return f"Order #{self.pk} - {self.customer.name}"

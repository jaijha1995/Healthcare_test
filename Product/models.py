from django.db import models
from restserver.utils import paginate_queryset, TimestampMixin

class Product(TimestampMixin):
    PRODUCT_TYPE_CHOICES = (
    ("TOP_RATED", "Top Rated Products"),
    ("NEW_ARRIVALS", "New Arrivals"),
    ("BEST_SELLERS", "Best Sellers"),
    ("Most Popular Products", "Most Popular Products"),
    ("Trending Products", "Trending Products"),
    )
    title_types = models.CharField(max_length=50,  choices=PRODUCT_TYPE_CHOICES, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    image = models.URLField()
    model_3d = models.URLField()
    size_tags = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    dfx_content = models.JSONField(blank=True, null=True)
    section = models.CharField(max_length=20, null=True, blank=True)


    class Meta:
        indexes = [
            models.Index(fields=["title_types"]),
            models.Index(fields=["name"]),
            models.Index(fields=["gender"]),
            models.Index(fields=["section"]),
        ]
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}"
    
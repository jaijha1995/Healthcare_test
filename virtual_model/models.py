from django.db import models

class Category(models.Model):
    TYPE_CHOICES = (
        ('category', 'Category'),
        ('subcategory', 'Sub Category'),
        ('subsubcategory', 'Sub Sub Category'),
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.type} - {self.name}"



class SubCategory(Category):
    class Meta:
        proxy = True
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"

# Virtual/Proxy model for Sub Sub Category
class SubSubCategory(Category):
    class Meta:
        proxy = True
        verbose_name = "Sub Sub Category"
        verbose_name_plural = "Sub Sub Categories"

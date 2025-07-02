from django.db import models
from superadmin.models import SuperAdmin

# Create your models here.

class Customer(models.Model):
    ROLES = (
        ('Customer', 'Customer'),
    )
    superadmin  = models.ForeignKey(SuperAdmin , on_delete=models.CASCADE , null=False , default='')
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200 , unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=200)
    re_password = models.CharField(max_length=200)
    otp = models.CharField(max_length=10 , null=True , blank=True)
    role = models.CharField(max_length=20, choices=ROLES)

    whatsapp = models.CharField(max_length=15)


    class Meta:
        db_table = "customer"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['last_name']),
            models.Index(fields=['mobile']),
        ]

    def __str__(self):
        return self.name + '   ' + self.last_name

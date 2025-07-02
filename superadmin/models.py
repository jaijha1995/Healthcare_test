from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password


class SuperAdmin(models.Model):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin')
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    repassword = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='superadmin')

    def __str__(self):
        return f"{self.role.capitalize()} - {self.email}"

    class Meta:
        db_table = "superadmin"

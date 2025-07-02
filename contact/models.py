from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()         # ✅ lowercase
    mobile = models.CharField(max_length=12)
    message = models.TextField()
    whatsapp = models.CharField(max_length=15)  # ✅ optional field



    class Meta:
        db_table = "contact"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['mobile']),
        ]

    def __str__(self):
        return self.name +  ' ' + self.email
    
    

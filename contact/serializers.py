# myapp/serializers.py
from rest_framework import serializers
from .models import Contact

class contactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'
        

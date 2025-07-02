from rest_framework import serializers
from .models import Customer
from superadmin.models import SuperAdmin
from django.contrib.auth.hashers import make_password

class CustomerSerializer(serializers.ModelSerializer):
    superadmin  = serializers.PrimaryKeyRelatedField(queryset=SuperAdmin.objects.all())
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        customer = Customer.objects.create(**validated_data)
        if password:
            customer.password = make_password(password)
            customer.save()
        
        return customer

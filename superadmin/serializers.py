# myapp/serializers.py
from rest_framework import serializers
from .models import SuperAdmin
from django.contrib.auth.hashers import make_password

class SuperAdminSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True)

    class Meta:
        model = SuperAdmin
        fields = '__all__'
        depth = 2

    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     customer = SuperAdmin.objects.create(**validated_data)
    #     if password:
    #         customer.password = make_password(password)
    #         customer.save()
        
    #     return customer

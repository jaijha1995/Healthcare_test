from rest_framework import serializers
from customer.models import Customer
from superadmin.models import SuperAdmin
from virtual_model.models import Category, SubCategory, SubSubCategory
from candidates.models import Candidate
from contact.models import Contact
from Product.models import Product
from .models import Order
from customer.serializers import CustomerSerializer
from superadmin.serializers import SuperAdminSerializer
from candidates.serializers import CandidateSerializer
from contact.serializers import contactSerializer
from Product.serializers import ProductSerializer
from virtual_model.serializers import CategorySerializer, SubCategorySerializer, SubSubCategorySerializer

class OrderSerializer(serializers.ModelSerializer):
    # Read-only nested data
    customer = CustomerSerializer(read_only=True)
    superadmin = SuperAdminSerializer(read_only=True)
    candidate = CandidateSerializer(read_only=True)
    contact = contactSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    subsubcategory = SubSubCategorySerializer(read_only=True)

    # Write using IDs
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True)
    superadmin_id = serializers.PrimaryKeyRelatedField(queryset=SuperAdmin.objects.all(), write_only=True)
    candidate_id = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all(), write_only=True)
    contact_id = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), write_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    subcategory_id = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), write_only=True)
    subsubcategory_id = serializers.PrimaryKeyRelatedField(queryset=SubSubCategory.objects.all(), write_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_date',
            'order_status',
            'total_amount',
            'customer', 'superadmin', 'candidate',
            'contact', 'product', 'category', 'subcategory', 'subsubcategory',
            'customer_id', 'superadmin_id', 'candidate_id',
            'contact_id', 'product_id', 'category_id',
            'subcategory_id', 'subsubcategory_id'
        ]
        read_only_fields = ['id', 'order_date']

    def create(self, validated_data):
        customer = validated_data.pop('customer_id')
        superadmin = validated_data.pop('superadmin_id')
        candidate = validated_data.pop('candidate_id')
        contact = validated_data.pop('contact_id')
        product = validated_data.pop('product_id')
        category = validated_data.pop('category_id')
        subcategory = validated_data.pop('subcategory_id')
        subsubcategory = validated_data.pop('subsubcategory_id')

        order = Order.objects.create(
            customer=customer,
            superadmin=superadmin,
            candidate=candidate,
            contact=contact,
            product=product,
            category=category,
            subcategory=subcategory,
            subsubcategory=subsubcategory,
            **validated_data
        )
        return order

    def update(self, instance, validated_data):
        instance.customer = validated_data.pop('customer_id', instance.customer)
        instance.superadmin = validated_data.pop('superadmin_id', instance.superadmin)
        instance.candidate = validated_data.pop('candidate_id', instance.candidate)
        instance.contact = validated_data.pop('contact_id', instance.contact)
        instance.product = validated_data.pop('product_id', instance.product)
        instance.category = validated_data.pop('category_id', instance.category)
        instance.subcategory = validated_data.pop('subcategory_id', instance.subcategory)
        instance.subsubcategory = validated_data.pop('subsubcategory_id', instance.subsubcategory)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

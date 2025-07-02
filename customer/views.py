from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from .models import Customer
import logging
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import secrets
from django.core.cache import cache
from .utils import generate_otp, send_otp_email
import pytz
import requests
from datetime import datetime, time
import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework.pagination import PageNumberPagination

class CustomerViews(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def generate_token_number(self):
        return secrets.token_hex(16)
    
    def send_welcome_email(self, email, first_name, last_name, password):
        subject = 'Welcome to Video Management system'
        html_message = render_to_string('welcome_email_template.html', {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
        })
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, 'jai@skylabstech.com', [email], html_message=html_message)

    def post(self, request, org_id=None):
        data = request.data
        logging.warning("Add customer")
        logging.warning(data)
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            customer = serializer.save()
            customer.save()
            self.send_welcome_email(customer.email, customer.name, customer.last_name, customer.re_password)
            
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            logging.warning(serializer.errors)
            return Response({"status": "Please provide mandatory fields", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            customer = Customer.objects.filter(id=id).first()
            if customer:
                serializer = CustomerSerializer(customer)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Filtering based on query parameters
        name = request.query_params.get('name', '')
        last_name = request.query_params.get('last_name', '')
        mobile = request.query_params.get('mobile', '')
        search = request.query_params.get('search', '')  # global search

        filters = Q()

        # ✅ Field-specific filters
        if name:
            filters &= Q(name__istartswith=name)
        if last_name:
            filters &= Q(last_name__istartswith=last_name)
        if mobile:
            filters &= Q(mobile__istartswith=mobile)

        # ✅ Global search filter — applies OR condition
        if search:
            search_filter = (
                Q(name__istartswith=search) |
                Q(last_name__istartswith=search) |
                Q(mobile__istartswith=search)
            )
            filters &= search_filter

        queryset = Customer.objects.filter(filters).order_by('id')

        # ✅ Pagination
        paginator = PageNumberPagination()
        page_size = request.query_params.get('page_size')
        if page_size and page_size.isdigit():
            paginator.page_size = int(page_size)
        else:
            paginator.page_size = 100  # default

        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = CustomerSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)

    def patch(self, request, id=None, org_id=None):
        id = request.data.get('id')
        item = Customer.objects.get(id=id)
        serializer = CustomerSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None, org_id=None):
        item = get_object_or_404(Customer, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})



class ListCustomerViews(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, org_id=None):
        items = Customer.objects.filter(org_id=org_id).only('id', 'first_name', 'last_name', 'email')
        serializer = CustomerSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)




class LoginCustomer(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomerSerializer

    def post(self, request, org_id=None):
        email = request.data['email']
        password = request.data['password']

        try:
            # Fetch the customer based on email
            item = Customer.objects.get(email=email)
            
            # Check if the password is correct
            if check_password(password, item.password):
                # Generate JWT tokens
                refresh = RefreshToken.for_user(item)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                
                # Serialize the customer data
                serializer = CustomerSerializer(item)
                data = serializer.data
                
                # Return the response with the JWT token
                return Response({
                    "status": "success",
                    "data": data,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "msg": "Login successful"
                })
            else:
                return Response({
                    "status": "failure", 
                    "msg": "Invalid credentials. Please check your email and password."
                })

        except Customer.DoesNotExist:
            return Response({
                "status": "failure", 
                "msg": "Email does not exist. Please check your email and try again."
            })
        

class OTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        send_otp_email(email, otp)
        customer.otp = otp
        customer.save()

        return Response({"otp": otp}, status=status.HTTP_200_OK)


class VerifyOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response({'error': 'Invalid email.'}, status=status.HTTP_400_BAD_REQUEST)

        if otp != customer.otp:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        customer.is_verified = True
        customer.save()

        return Response({'message': 'OTP verified successfully.'})


class SendSMSAPIView(APIView):
    def post(self, request):
        url = "https://www.fast2sms.com/dev/bulkV2"
        mobile = request.data.get('mobile')

        if not mobile:
            return Response({"error": "Mobile number is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = Customer.objects.filter(mobile=mobile).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        otp = str(random.randint(100000, 999999))
        payload = f"variables_values={otp}&route=otp&numbers={mobile}"
        headers = {
            'authorization': "5GrHl3TveRQV2I6NwSfYCzFj01JXdLxWkBnAM4ut8pagcbPm9ODNrALnQ1bR5yUYCOd7xSK9PklHzfjG",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }

        try:
            response = requests.post(url, data=payload, headers=headers)
            response_data = response.json()

            if response_data.get("return") is False:
                return Response({"error": "Spamming detected."}, status=status.HTTP_400_BAD_REQUEST)

            user.otp = otp
            user.save()
            return Response({"success": True, "message": "OTP sent successfully."}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": "Failed to send SMS", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MobileVerifyOTP(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')

        if not mobile or not otp:
            return Response({'error': 'Mobile number and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(mobile=mobile, otp=otp)
        except Customer.DoesNotExist:
            return Response({'error': 'Invalid OTP or mobile number.'}, status=status.HTTP_400_BAD_REQUEST)

        customer.otp = None
        customer.is_verified = True
        customer.save()

        return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import Customer

class ForgotPasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        repassword = request.data.get('repassword')

        # Step 1: Check if email exists
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Step 2: Ensure password and repassword are provided
        if not password or not repassword:
            return Response({"message": "Email verified. Provide password and repassword to reset your password."},
                            status=status.HTTP_200_OK)

        # Step 3: Validate password and repassword
        if password != repassword:
            return Response({"error": "Password and repassword do not match"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 4: Update password and repassword in the database
        customer.password = make_password(password)  # Hash the password for security
        customer.re_password = repassword  # Store the raw repassword
        customer.save(update_fields=["password", "re_password"])  # Save only the updated fields

        return Response({"message": "Password reset successful", "status": "success"}, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SuperAdmin
from .serializers import SuperAdminSerializer
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token

class SuperAdminPagination(PageNumberPagination):
    page_size = 10

class SuperAdminListView(APIView):
    
    def get(self, request, id=None):
        data = {}
        role_filter = request.query_params.get('role', None)  # Get role from query parameters
        
        if id is not None:
            try:
                customer = SuperAdmin.objects.get(id=id)
                serializer = SuperAdminSerializer(customer)
                data = serializer.data
            except SuperAdmin.DoesNotExist:
                return Response({"status": "error", "message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            if role_filter:
                # Filter customers by role if 'role' query parameter is provided
                customers = SuperAdmin.objects.filter(role=role_filter).order_by('id')
            else:
                # Otherwise, get all customers
                customers = SuperAdmin.objects.all().order_by('id')
            
            serializer = SuperAdminSerializer(customers, many=True)
            data['data'] = serializer.data

        data["status"] = "success"
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # Ensure role is included in the request data
        role = request.data.get('role', None)
        if role not in ['superadmin', 'admin', 'user']:  # Validate role
            return Response({"status": "error", "message": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = SuperAdminSerializer(data=request.data)
        
        if serializer.is_valid():
            # Set the password before saving
            password = serializer.validated_data.get('password')
            serializer.save()  # Save the object
            superadmin_instance = serializer.instance
            superadmin_instance.set_password(password)  # Hash the password
            superadmin_instance.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SuperAdminDetailView(APIView):
    def get(self, request, pk):
        try:
            superadmin = SuperAdmin.objects.get(pk=pk)
            serializer = SuperAdminSerializer(superadmin)
            return Response(serializer.data)
        except SuperAdmin.DoesNotExist:
            return Response({"error": "SuperAdmin not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            superadmin = SuperAdmin.objects.get(pk=pk)
        except SuperAdmin.DoesNotExist:
            return Response({"error": "SuperAdmin not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SuperAdminSerializer(superadmin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            superadmin = SuperAdmin.objects.get(pk=pk)
            superadmin.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SuperAdmin.DoesNotExist:
            return Response({"error": "SuperAdmin not found"}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

class Loginsuperadmin(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SuperAdminSerializer
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {"status": "error", "msg": "Both email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            item = SuperAdmin.objects.filter(email=email).first()
            if not item:
                return Response(
                    {"status": "email error", "msg": "Email not found."},
                    status=status.HTTP_200_OK
                )
            refresh = RefreshToken.for_user(item)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            serializer = SuperAdminSerializer(item)
            dpassword = serializer.data['password']

            if password != dpassword:
                return Response(
                    {"status": "passworderror", "msg": "Passwords do not match, try again."},
                    status=status.HTTP_200_OK
                )
            data = serializer.data
            return Response({
                    "status": "success",
                    "data": data,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "msg": "Login successful"
                })
        
        except SuperAdmin.DoesNotExist:
            return Response(
                {"status": "error", "msg": "An error occurred."},
                status=status.HTTP_400_BAD_REQUEST
            )